"""
Log format parsers for different languages and frameworks.
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import re
import json


@dataclass
class LogEntry:
    """Represents a single log entry."""
    timestamp: Optional[datetime]
    level: str  # ERROR, WARN, INFO, DEBUG
    message: str
    stack_trace: Optional[str] = None
    source: Optional[str] = None  # File/line where error occurred
    metadata: Optional[Dict] = None
    raw_log: str = ""


class LogParser:
    """Base parser with auto-detection."""
    
    def __init__(self):
        self.parsers = {
            'nodejs_winston': WinstonParser(),
            'nodejs_pino': PinoParser(),
            'python_logging': PythonLoggingParser(),
            'python_structlog': StructlogParser(),
            'go_standard': GoStandardParser(),
        }
    
    def parse(self, log_content: str) -> List[LogEntry]:
        """Parse log content with auto-format detection."""
        lines = log_content.strip().split('\n')
        
        # Try to detect format from first few lines
        sample = '\n'.join(lines[:10])
        format_type = self._detect_format(sample)
        
        if format_type and format_type in self.parsers:
            return self.parsers[format_type].parse(log_content)
        
        # Fallback to generic parser
        return GenericParser().parse(log_content)
    
    def _detect_format(self, sample: str) -> Optional[str]:
        """Detect log format from sample."""
        # Try JSON formats first
        first_line = sample.strip().split('\n')[0]
        if first_line.startswith('{'):
            try:
                data = json.loads(first_line)
                # Check for Pino format (has 'time' and 'msg')
                if 'time' in data and 'msg' in data:
                    return 'nodejs_pino'
                # Check for Winston format (has 'level' and 'message')
                elif 'level' in data and 'message' in data:
                    return 'nodejs_winston'
            except:
                pass
        
        # Check for Python logging format
        # Format: 2026-03-06 14:23:11,456 - module.name - LEVEL - message
        if re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} - [\w.]+ -', sample):
            return 'python_logging'
        
        # Check for Go standard format
        if re.search(r'\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}', sample):
            return 'go_standard'
        
        # For other formats, use generic parser
        return None


class WinstonParser:
    """Parser for Winston logger (Node.js) - JSON format."""
    
    def parse(self, log_content: str) -> List[LogEntry]:
        entries = []
        for line in log_content.strip().split('\n'):
            if not line.strip():
                continue
            
            try:
                data = json.loads(line)
                entry = LogEntry(
                    timestamp=self._parse_timestamp(data.get('timestamp')),
                    level=data.get('level', 'info').upper(),
                    message=data.get('message', ''),
                    stack_trace=data.get('stack'),
                    source=self._extract_source(data.get('stack')),
                    metadata={k: v for k, v in data.items() 
                             if k not in ['timestamp', 'level', 'message', 'stack']},
                    raw_log=line
                )
                entries.append(entry)
            except json.JSONDecodeError:
                continue
        
        return entries
    
    def _parse_timestamp(self, ts: Optional[str]) -> Optional[datetime]:
        if not ts:
            return None
        try:
            return datetime.fromisoformat(ts.replace('Z', '+00:00'))
        except:
            return None
    
    def _extract_source(self, stack: Optional[str]) -> Optional[str]:
        if not stack:
            return None
        # Extract first line from stack trace
        match = re.search(r'at .+ \((.+):\d+:\d+\)', stack)
        return match.group(1) if match else None


class PinoParser:
    """Parser for Pino logger (Node.js) - JSON format."""
    
    def parse(self, log_content: str) -> List[LogEntry]:
        entries = []
        for line in log_content.strip().split('\n'):
            if not line.strip():
                continue
            
            try:
                data = json.loads(line)
                entry = LogEntry(
                    timestamp=datetime.fromtimestamp(data.get('time', 0) / 1000),
                    level=self._level_to_string(data.get('level', 30)),
                    message=data.get('msg', ''),
                    stack_trace=data.get('stack') or data.get('err', {}).get('stack'),
                    source=self._extract_source(data.get('stack')),
                    metadata={k: v for k, v in data.items() 
                             if k not in ['time', 'level', 'msg', 'stack', 'err']},
                    raw_log=line
                )
                entries.append(entry)
            except (json.JSONDecodeError, ValueError):
                continue
        
        return entries
    
    def _level_to_string(self, level: int) -> str:
        levels = {10: 'TRACE', 20: 'DEBUG', 30: 'INFO', 40: 'WARN', 50: 'ERROR', 60: 'FATAL'}
        return levels.get(level, 'INFO')
    
    def _extract_source(self, stack: Optional[str]) -> Optional[str]:
        if not stack:
            return None
        match = re.search(r'at .+ \((.+):\d+:\d+\)', stack)
        return match.group(1) if match else None


class PythonLoggingParser:
    """Parser for Python logging module."""
    
    def parse(self, log_content: str) -> List[LogEntry]:
        entries = []
        current_entry = None
        current_stack = []
        in_stack_trace = False
        
        for line in log_content.split('\n'):
            # Try to parse as new log entry
            # Format: 2026-03-06 14:23:11,456 - module.name - LEVEL - message
            # Or: 2026-03-06 14:23:11,456 - LEVEL - message (without module)
            match = re.match(
                r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - (?:([\w.]+) - )?(\w+) - (.+)',
                line
            )
            
            if match:
                # Save previous entry if exists
                if current_entry:
                    if current_stack:
                        current_entry.stack_trace = '\n'.join(current_stack)
                    entries.append(current_entry)
                
                # Start new entry
                timestamp_str, module, level, message = match.groups()
                current_entry = LogEntry(
                    timestamp=datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S,%f'),
                    level=level.upper(),
                    message=message.strip(),
                    raw_log=line
                )
                current_stack = []
                in_stack_trace = False
            elif current_entry:
                # Check if this is the start of a traceback
                if 'Traceback (most recent call last):' in line:
                    in_stack_trace = True
                    current_stack.append(line)
                # If we're in a stack trace, add all subsequent lines until we hit a new log entry
                elif in_stack_trace:
                    current_stack.append(line)
                # Also check for indented lines (part of stack trace)
                elif line.startswith(('  ', '\t')):
                    current_stack.append(line)
                    in_stack_trace = True
        
        # Add last entry
        if current_entry:
            if current_stack:
                current_entry.stack_trace = '\n'.join(current_stack)
            entries.append(current_entry)
        
        return entries


class StructlogParser:
    """Parser for structlog (Python)."""
    
    def parse(self, log_content: str) -> List[LogEntry]:
        entries = []
        for line in log_content.strip().split('\n'):
            if not line.strip():
                continue
            
            try:
                data = json.loads(line)
                entry = LogEntry(
                    timestamp=datetime.fromisoformat(data.get('timestamp', '')),
                    level=data.get('level', 'info').upper(),
                    message=data.get('event', ''),
                    stack_trace=data.get('exception'),
                    source=data.get('file'),
                    metadata={k: v for k, v in data.items() 
                             if k not in ['timestamp', 'level', 'event', 'exception', 'file']},
                    raw_log=line
                )
                entries.append(entry)
            except (json.JSONDecodeError, ValueError):
                continue
        
        return entries


class GoStandardParser:
    """Parser for Go standard library log."""
    
    def parse(self, log_content: str) -> List[LogEntry]:
        entries = []
        for line in log_content.strip().split('\n'):
            if not line.strip():
                continue
            
            # Format: 2009/01/23 01:23:23 message
            match = re.match(
                r'(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}) (.+)',
                line
            )
            
            if match:
                timestamp_str, message = match.groups()
                
                # Detect level from message
                level = 'INFO'
                if 'ERROR' in message or 'error' in message:
                    level = 'ERROR'
                elif 'WARN' in message or 'warn' in message:
                    level = 'WARN'
                elif 'DEBUG' in message or 'debug' in message:
                    level = 'DEBUG'
                
                entry = LogEntry(
                    timestamp=datetime.strptime(timestamp_str, '%Y/%m/%d %H:%M:%S'),
                    level=level,
                    message=message.strip(),
                    raw_log=line
                )
                entries.append(entry)
        
        return entries


class GenericParser:
    """Fallback parser for unknown formats."""
    
    def parse(self, log_content: str) -> List[LogEntry]:
        entries = []
        for line in log_content.strip().split('\n'):
            if not line.strip():
                continue
            
            # Try to extract basic info
            level = 'INFO'
            if 'ERROR' in line.upper():
                level = 'ERROR'
            elif 'WARN' in line.upper():
                level = 'WARN'
            elif 'DEBUG' in line.upper():
                level = 'DEBUG'
            
            entry = LogEntry(
                timestamp=None,
                level=level,
                message=line.strip(),
                raw_log=line
            )
            entries.append(entry)
        
        return entries
