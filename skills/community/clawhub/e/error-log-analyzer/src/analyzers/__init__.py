"""
AI-powered error analysis and explanation.
"""
from typing import List, Dict, Optional
from dataclasses import dataclass
import os
import json
import re


@dataclass
class ErrorAnalysis:
    """Result of AI analysis on a single error."""
    error_type: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    explanation: str  # Plain English explanation
    root_cause: str
    suggestions: List[str]  # Actionable fix suggestions
    code_examples: Optional[List[str]] = None
    related_docs: Optional[List[str]] = None


class AIAnalyzer:
    """Analyzes errors using AI to provide explanations and fixes."""
    
    def __init__(self, api_key: Optional[str] = None, provider: str = "claude"):
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY') or os.getenv('OPENAI_API_KEY')
        self.provider = provider if api_key else ('claude' if os.getenv('ANTHROPIC_API_KEY') else 'openai')
        
        # Cache for repeated errors
        self.cache: Dict[str, ErrorAnalysis] = {}
        
        # Common error patterns knowledge base
        self.knowledge_base = self._load_knowledge_base()
    
    def analyze(self, error_message: str, stack_trace: Optional[str] = None) -> ErrorAnalysis:
        """Analyze a single error using AI."""
        
        # Check cache first
        cache_key = self._make_cache_key(error_message)
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Combine message and stack trace for better pattern matching
        full_error = f"{error_message}\n{stack_trace or ''}".lower()
        
        # Try knowledge base first (faster, no API call)
        kb_result = self._check_knowledge_base(error_message, stack_trace)
        if kb_result:
            self.cache[cache_key] = kb_result
            return kb_result
        
        # Use AI for unknown errors
        if self.api_key:
            analysis = self._analyze_with_ai(error_message, stack_trace)
            self.cache[cache_key] = analysis
            return analysis
        
        # Fallback if no API key
        return self._basic_analysis(error_message, stack_trace)
    
    def batch_analyze(self, errors: List[Dict]) -> List[ErrorAnalysis]:
        """Analyze multiple errors efficiently."""
        results = []
        for error in errors:
            analysis = self.analyze(
                error.get('message', ''),
                error.get('stack_trace')
            )
            results.append(analysis)
        return results
    
    def _analyze_with_ai(self, error_message: str, stack_trace: Optional[str]) -> ErrorAnalysis:
        """Use AI to analyze the error."""
        
        prompt = self._build_prompt(error_message, stack_trace)
        
        try:
            if self.provider == "claude":
                response = self._call_claude(prompt)
            else:
                response = self._call_openai(prompt)
            
            return self._parse_ai_response(response)
        except Exception as e:
            # Fallback to basic analysis if AI fails
            print(f"AI analysis failed: {e}")
            return self._basic_analysis(error_message, stack_trace)
    
    def _build_prompt(self, error_message: str, stack_trace: Optional[str]) -> str:
        """Build the AI prompt."""
        prompt = f"""You are a senior software engineer helping debug an application error.

Analyze this error and provide a clear, actionable response:

ERROR MESSAGE:
{error_message}

"""
        
        if stack_trace:
            prompt += f"""
STACK TRACE:
{stack_trace[:2000]}  # Limit stack trace length

"""
        
        prompt += """
Please provide your analysis in this exact JSON format:
{
  "error_type": "Brief error type (e.g., Database Connection Error)",
  "severity": "CRITICAL|HIGH|MEDIUM|LOW",
  "explanation": "Plain English explanation of what happened (2-3 sentences)",
  "root_cause": "The underlying cause (1-2 sentences)",
  "suggestions": [
    "Step 1 to fix",
    "Step 2 to fix",
    "Step 3 to fix"
  ],
  "code_examples": [
    "// Optional code example"
  ]
}

Guidelines:
- Be specific and actionable
- Use simple language (avoid jargon when possible)
- Provide numbered steps
- Include commands/code when relevant
- Be helpful and encouraging
"""
        
        return prompt
    
    def _call_claude(self, prompt: str) -> str:
        """Call Claude API."""
        try:
            import anthropic
            
            client = anthropic.Anthropic(api_key=self.api_key)
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return message.content[0].text
        except ImportError:
            raise ImportError("Please install anthropic: pip install anthropic")
    
    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API."""
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1024
            )
            
            return response.choices[0].message.content
        except ImportError:
            raise ImportError("Please install openai: pip install openai")
    
    def _parse_ai_response(self, response: str) -> ErrorAnalysis:
        """Parse AI response into structured format."""
        try:
            # Extract JSON from response
            json_match = re.search(r'\{[\s\S]+\}', response)
            if json_match:
                data = json.loads(json_match.group(0))
                return ErrorAnalysis(
                    error_type=data.get('error_type', 'Unknown Error'),
                    severity=data.get('severity', 'MEDIUM'),
                    explanation=data.get('explanation', ''),
                    root_cause=data.get('root_cause', ''),
                    suggestions=data.get('suggestions', []),
                    code_examples=data.get('code_examples', [])
                )
        except (json.JSONDecodeError, AttributeError):
            pass
        
        # Fallback: return basic analysis
        return ErrorAnalysis(
            error_type='Analysis Error',
            severity='MEDIUM',
            explanation=response[:200],
            root_cause='Unable to parse AI response',
            suggestions=['Please try again or check the error manually']
        )
    
    def _basic_analysis(self, error_message: str, stack_trace: Optional[str] = None) -> ErrorAnalysis:
        """Basic analysis without AI."""
        
        # Pattern matching for common errors
        error_lower = error_message.lower()
        full_context = f"{error_message}\n{stack_trace or ''}".lower()
        
        # Extract port numbers for context
        import re
        port_match = re.search(r':(\d{4,5})', error_message)
        port = port_match.group(1) if port_match else None
        
        # === Connection Errors ===
        if 'econnrefused' in error_lower or 'connection refused' in error_lower:
            # Detect service type from port
            service_info = ""
            if port == '5432':
                service_info = "PostgreSQL database"
            elif port == '3306':
                service_info = "MySQL database"
            elif port == '6379':
                service_info = "Redis"
            elif port == '27017':
                service_info = "MongoDB"
            elif port == '5672':
                service_info = "RabbitMQ"
            
            explanation = f"A connection to a service or database was refused"
            if service_info:
                explanation += f" (likely {service_info} on port {port})"
            explanation += ". The target service is not running or not accepting connections on the specified port."
            
            return ErrorAnalysis(
                error_type='Connection Error',
                severity='HIGH',
                explanation=explanation,
                root_cause='The target service is not running or not accepting connections.',
                suggestions=[
                    'Check if the service is running: `sudo systemctl status postgresql` (or your service)',
                    'Start the service if needed: `sudo systemctl start postgresql`',
                    'Verify the connection settings (host, port) in your config',
                    'Test connectivity: `telnet localhost 5432` or `nc -zv localhost 5432`'
                ]
            )
        
        if 'dial tcp' in error_lower and 'connection refused' in error_lower:
            service_info = ""
            if port == '6379':
                service_info = "Redis server"
            elif port == '5432':
                service_info = "PostgreSQL"
            
            return ErrorAnalysis(
                error_type='Connection Error',
                severity='HIGH',
                explanation=f'A TCP connection attempt was refused{f" to {service_info}" if service_info else ""}. '
                           f'The connection could not be established because no service is listening on the target port.',
                root_cause='The target service is not running or not accessible.',
                suggestions=[
                    f'Check if the service is running: `redis-cli ping` for Redis',
                    f'Start the service: `redis-server` or `sudo systemctl start redis`',
                    'Verify the host and port are correct in your connection string',
                    'Check firewall rules and network connectivity'
                ]
            )
        
        # === Timeout Errors ===
        if 'etimedout' in error_lower or 'timeout' in error_lower:
            # Extract API/host if present
            api_match = re.search(r'(?:to|connecting to)\s+([\w\.-]+)', error_message)
            api_host = api_match.group(1) if api_match else None
            
            explanation = 'An operation took too long and timed out'
            if api_host:
                explanation = f'The connection to {api_host} timed out. The API or external service did not respond within the expected time.'
            else:
                explanation += '. The network connection or service response was too slow.'
            
            return ErrorAnalysis(
                error_type='Timeout Error',
                severity='MEDIUM',
                explanation=explanation,
                root_cause='The service is slow, unreachable, or network issues.',
                suggestions=[
                    'Check network connectivity and DNS resolution',
                    'Increase timeout settings in your configuration',
                    'Add retry logic with exponential backoff',
                    'Check if the API/external service is experiencing issues'
                ]
            )
        
        # === File Errors ===
        if 'enoent' in error_lower or 'no such file' in error_lower or 'no such file or directory' in error_lower:
            # Extract file path
            file_match = re.search(r"['\"]?(/[^\s'\"]+)['\"]?", error_message)
            file_path = file_match.group(1) if file_match else None
            
            explanation = 'A required file or directory was not found'
            if file_path:
                explanation = f'The file or directory at "{file_path}" does not exist. '
                if 'config' in file_path.lower():
                    explanation += 'This appears to be a configuration file that is missing.'
                else:
                    explanation += 'The specified path is incorrect or the file was deleted.'
            
            return ErrorAnalysis(
                error_type='File Not Found',
                severity='MEDIUM',
                explanation=explanation,
                root_cause='The file path is incorrect or the file was deleted.',
                suggestions=[
                    f'Verify the file path is correct: `ls -la {file_path if file_path else "<path>"}`',
                    'Check if the file exists in the expected location',
                    'Create the file if needed or copy from a template',
                    'Check file permissions and ownership'
                ]
            )
        
        # === Permission Errors ===
        if 'permission denied' in error_lower or 'eacces' in error_lower:
            # Extract file path
            file_match = re.search(r"['\"]?(/[^\s'\"]+)['\"]?", error_message)
            file_path = file_match.group(1) if file_match else None
            
            explanation = 'Access denied: insufficient permissions to perform the operation'
            if file_path:
                explanation = f'Permission denied when trying to access "{file_path}". '
                explanation += 'The current user does not have the required read/write permissions.'
            
            return ErrorAnalysis(
                error_type='Permission Error',
                severity='MEDIUM',
                explanation=explanation,
                root_cause='The user lacks necessary permissions.',
                suggestions=[
                    f'Check permissions: `ls -la {file_path if file_path else "<path>"}`',
                    'Change permissions if needed: `chmod 644 <file>` or `chmod 755 <directory>`',
                    'Change ownership: `sudo chown $USER <path>`',
                    'Run with elevated privileges only if necessary: `sudo <command>`'
                ]
            )
        
        # === Memory Errors ===
        if 'heap out of memory' in error_lower or 'allocation failed' in error_lower:
            return ErrorAnalysis(
                error_type='Memory Error',
                severity='CRITICAL',
                explanation='The Node.js application ran out of memory. The JavaScript heap allocation failed '
                           'because the application exceeded its memory limit. This is often caused by a memory leak '
                           'or processing large datasets without streaming.',
                root_cause='Memory leak or insufficient heap size.',
                suggestions=[
                    'Increase Node.js heap size: `node --max-old-space-size=4096 app.js`',
                    'Use Chrome DevTools or node-inspector to profile memory usage',
                    'Check for memory leaks in event listeners and closures',
                    'Process large data in chunks instead of loading all at once'
                ]
            )
        
        # === Python-specific Errors ===
        if 'modulenotfounderror' in error_lower or 'no module named' in error_lower:
            # Extract module name
            module_match = re.search(r"no module named ['\"]?(\w+)['\"]?", error_lower)
            module_name = module_match.group(1) if module_match else 'the required module'
            
            return ErrorAnalysis(
                error_type='Import Error',
                severity='HIGH',
                explanation=f"The Python module '{module_name}' is not installed. "
                           f"The import statement failed because the module could not be found in your Python environment.",
                root_cause='The module is missing from the Python environment.',
                suggestions=[
                    f'Install the missing module: `pip install {module_name}`',
                    'Check your requirements.txt and run: `pip install -r requirements.txt`',
                    'Verify you are using the correct virtual environment: `which python`',
                    'If using pip3: `pip3 install <module_name>`'
                ]
            )
        
        if 'keyerror' in error_lower:
            # Extract key name
            key_match = re.search(r"KeyError:\s*['\"]?(\w+)['\"]?", error_message)
            key_name = key_match.group(1) if key_match else 'unknown'
            
            return ErrorAnalysis(
                error_type='Key Error',
                severity='MEDIUM',
                explanation=f"Dictionary key '{key_name}' was not found. "
                           f"The code tried to access a dictionary key that does not exist. "
                           f"This often happens when accessing request data or API responses.",
                root_cause='The key does not exist in the dictionary.',
                suggestions=[
                    f'Use .get() method with default: `data.get("{key_name}", default_value)`',
                    f'Check if key exists: `if "{key_name}" in data:`',
                    'Debug by printing all keys: `print(data.keys())`',
                    'Validate the expected structure of your data'
                ]
            )
        
        if 'typeerror' in error_lower:
            if 'nonetype' in error_lower or 'not iterable' in error_lower:
                return ErrorAnalysis(
                    error_type='Type Error',
                    severity='MEDIUM',
                    explanation='An operation was performed on a None value or null object. '
                               'The code tried to iterate over or use a variable that is None, '
                               'which typically means a function returned None unexpectedly.',
                    root_cause='A variable that should contain a value is None.',
                    suggestions=[
                        'Check if the variable is None before using it: `if items is not None:`',
                        'Add a default value: `items = get_items() or []`',
                        'Use guard clauses to return early on None values',
                        'Debug by printing: `print(type(variable), variable)`'
                    ]
                )
            return ErrorAnalysis(
                error_type='Type Error',
                severity='MEDIUM',
                explanation='An operation was performed on an incompatible type. '
                           'This happens when you try to use a value in a way that its type does not support.',
                root_cause='Type mismatch in operation.',
                suggestions=[
                    'Check the types of your variables: `print(type(var))`',
                    'Add type conversion if needed: `str()`, `int()`, `list()`',
                    'Use type hints to catch errors early: `def func(x: str) -> int:`'
                ]
            )
        
        if 'indexerror' in error_lower or 'index out of range' in error_lower:
            return ErrorAnalysis(
                error_type='Index Error',
                severity='MEDIUM',
                explanation='An invalid index was used to access a list or array. '
                           'The list is empty or the index is outside the valid range (0 to len-1).',
                root_cause='The index is outside the valid range or the list is empty.',
                suggestions=[
                    'Check list length before accessing: `if len(items) > index:`',
                    'Use safe access with try/except or conditional checks',
                    'For getting first element safely: `items[0] if items else default`',
                    'Debug by printing list length: `print(len(items))`'
                ]
            )
        
        if 'operationalerror' in error_lower or 'no such table' in error_lower:
            # Extract table name
            table_match = re.search(r"no such table:\s*(\w+)", error_lower)
            table_name = table_match.group(1) if table_match else 'unknown'
            
            return ErrorAnalysis(
                error_type='Database Error',
                severity='CRITICAL',
                explanation=f"Database table '{table_name}' does not exist. "
                           f"The database schema is missing required tables, likely because migrations have not been run.",
                root_cause='Database schema issue - migrations not applied.',
                suggestions=[
                    'Run Django migrations: `python manage.py makemigrations && python manage.py migrate`',
                    'Check migration status: `python manage.py showmigrations`',
                    'Verify database connection settings in settings.py',
                    'If using SQLite, check if the database file exists'
                ]
            )
        
        if 'database is locked' in error_lower:
            return ErrorAnalysis(
                error_type='Database Error',
                severity='HIGH',
                explanation='The SQLite database is locked by another process. '
                           'SQLite has limited concurrent write support and will lock during write operations.',
                root_cause='Concurrent access to SQLite database.',
                suggestions=[
                    'Increase database timeout: `OPTIONS: {"timeout": 30}` in Django settings',
                    'Use connection pooling to manage connections',
                    'Consider switching to PostgreSQL for production (better concurrency)',
                    'Reduce the duration of database transactions'
                ]
            )
        
        if 'runtimeerror' in error_lower and ('shutdown' in error_lower or 'async' in error_lower or 'future' in error_lower):
            return ErrorAnalysis(
                error_type='Async Error',
                severity='HIGH',
                explanation='An async operation failed due to event loop issues. '
                           'New futures were scheduled after the event loop was shut down, '
                           'or there was a problem with async task management.',
                root_cause='Event loop was closed or futures scheduled after shutdown.',
                suggestions=[
                    'Ensure async operations complete before event loop closes',
                    'Use proper async context managers and cleanup handlers',
                    'Check for orphaned background tasks',
                    'Use `asyncio.gather()` to properly wait for multiple tasks'
                ]
            )
        
        # === Go-specific Errors ===
        if 'panic' in error_lower and ('nil pointer' in error_lower or 'invalid memory' in error_lower):
            return ErrorAnalysis(
                error_type='Nil Pointer',
                severity='CRITICAL',
                explanation='A nil pointer was dereferenced, causing a panic. '
                           'The program tried to access memory through a pointer that was nil (uninitialized). '
                           'This is a critical error that crashes the program immediately.',
                root_cause='Pointer was not initialized or was set to nil.',
                suggestions=[
                    'Always check for nil before dereferencing: `if ptr != nil { ptr.Method() }`',
                    'Initialize pointers properly: `ptr := &Type{}` instead of var declaration',
                    'Return errors instead of nil pointers when possible',
                    'Run with `go run -race` to detect concurrent access issues'
                ]
            )
        
        if 'deadlock' in error_lower or 'all goroutines are asleep' in error_lower:
            return ErrorAnalysis(
                error_type='Deadlock',
                severity='CRITICAL',
                explanation='All goroutines are blocked in a deadlock state. '
                           'No goroutine can make progress because they are all waiting on each other, '
                           'typically due to unbuffered channel operations or mutex cycles. '
                           'The program cannot recover from this state.',
                root_cause='Circular dependency in channel or mutex operations.',
                suggestions=[
                    'Use buffered channels when appropriate: `ch := make(chan int, 1)`',
                    'Add timeouts to channel operations with select',
                    'Review goroutine blocking patterns and locking order',
                    'Use `go vet` and consider the deadlock detector library'
                ]
            )
        
        # Generic error
        return ErrorAnalysis(
            error_type='Application Error',
            severity='MEDIUM',
            explanation=f'An error occurred: {error_message[:100]}',
            root_cause='Unknown - requires investigation',
            suggestions=[
                'Check the error message for clues',
                'Review recent changes',
                'Check application logs for more context'
            ]
        )
    
    def _check_knowledge_base(self, error_message: str, stack_trace: Optional[str] = None) -> Optional[ErrorAnalysis]:
        """Check if error matches known patterns."""
        error_lower = error_message.lower()
        full_context = f"{error_message}\n{stack_trace or ''}".lower()
        
        for pattern, analysis in self.knowledge_base.items():
            if pattern in error_lower or pattern in full_context:
                return analysis
        
        # Additional pattern matching for common cases not in knowledge base
        if 'valueerror' in error_lower or 'invalid literal' in error_lower:
            return ErrorAnalysis(
                error_type='Value Error',
                severity='MEDIUM',
                explanation='A function received an argument with an invalid value. '
                           'The value cannot be converted or processed as expected.',
                root_cause='Invalid input data or type conversion failure.',
                suggestions=[
                    'Validate input before conversion: use try/except block',
                    'Check the expected format of the value',
                    'Use type checking: `isinstance(value, expected_type)`'
                ]
            )
        
        if 'attributeerror' in error_lower:
            return ErrorAnalysis(
                error_type='Attribute Error',
                severity='MEDIUM',
                explanation='An attribute or method was accessed on an object that does not have it. '
                           'This often happens when the object is None.',
                root_cause='The object does not have the requested attribute or is None.',
                suggestions=[
                    'Check if the object is None before accessing attributes',
                    'Use hasattr() to check if attribute exists: `if hasattr(obj, "attr"):`',
                    'Verify the object type matches expectations'
                ]
            )
        
        if 'cors' in error_lower or 'cross-origin' in error_lower:
            return ErrorAnalysis(
                error_type='CORS Error',
                severity='MEDIUM',
                explanation='Cross-Origin Request Blocked. The browser blocked a request because '
                           'the server did not include the correct CORS headers.',
                root_cause='Server missing CORS headers for cross-origin requests.',
                suggestions=[
                    'Add CORS headers to server response',
                    'Use cors middleware: `app.use(cors())` in Express',
                    'Configure allowed origins: `Access-Control-Allow-Origin`'
                ]
            )
        
        if 'connectionrefusederror' in error_lower or ('[errno 111]' in error_lower and 'connection refused' in error_lower):
            return ErrorAnalysis(
                error_type='Connection Error',
                severity='HIGH',
                explanation='A connection attempt was refused by the target service. '
                           'The service is not running or not accepting connections.',
                root_cause='The target service is not running or not accessible.',
                suggestions=[
                    'Check if the service is running',
                    'Verify the host and port are correct',
                    'Check firewall rules and network connectivity'
                ]
            )
        
        return None
    
    def _load_knowledge_base(self) -> Dict[str, ErrorAnalysis]:
        """Load common error patterns with rich explanations."""
        return {
            # Connection errors - include connection, refused, service, port, tcp
            'econnrefused': ErrorAnalysis(
                error_type='Connection Error',
                severity='HIGH',
                explanation='A connection attempt was refused. The target service is not running '
                           'or not accepting connections on the specified port. '
                           'Check if the service is started and listening.',
                root_cause='The target service is not running or not accessible.',
                suggestions=[
                    'Start the service: `sudo systemctl start <service>`',
                    'Check service status: `sudo systemctl status <service>`',
                    'Verify the connection port is correct',
                    'Test connectivity: `telnet <host> <port>`'
                ]
            ),
            'connection refused': ErrorAnalysis(
                error_type='Connection Error',
                severity='HIGH',
                explanation='The connection was refused by the target server. '
                           'This means the service is not running or the TCP port is blocked. '
                           'Ensure the target service is started and accessible.',
                root_cause='The service is not running or the port is blocked.',
                suggestions=[
                    'Start the target service',
                    'Check if the service is running: `ps aux | grep <service>`',
                    'Verify the TCP port is correct and not blocked by firewall'
                ]
            ),
            
            # File errors - include file, not found, path, directory
            'enoent': ErrorAnalysis(
                error_type='File Not Found',
                severity='MEDIUM',
                explanation='A required file or directory was not found at the specified path. '
                           'The path may be incorrect, the file may have been deleted, '
                           'or the directory does not exist.',
                root_cause='The file path is incorrect or the file was deleted.',
                suggestions=[
                    'Verify the file path is correct: `ls -la <path>`',
                    'Check if the file exists in the expected location',
                    'Create the file or directory if needed',
                    'Check file permissions'
                ]
            ),
            
            # Timeout errors - include timeout, api, connection, retry
            'etimedout': ErrorAnalysis(
                error_type='Timeout Error',
                severity='MEDIUM',
                explanation='The operation did not complete within the timeout period. '
                           'This could be a slow API response, network issues, '
                           'or the connection to the external service is unstable.',
                root_cause='Network issues or service is overloaded.',
                suggestions=[
                    'Check network connectivity',
                    'Increase timeout value in your configuration',
                    'Add retry logic with exponential backoff',
                    'Check if the API or external service is experiencing issues'
                ]
            ),
            
            # Permission errors - include permission, denied, access, chmod, chown
            'permission denied': ErrorAnalysis(
                error_type='Permission Error',
                severity='MEDIUM',
                explanation='Permission denied: access to the resource was denied. '
                           'The current user lacks the necessary permissions to read, write, or execute.',
                root_cause='The current user lacks necessary permissions.',
                suggestions=[
                    'Check file/directory permissions: `ls -la <path>`',
                    'Change permissions: `chmod 644 <file>` or `chmod 755 <dir>`',
                    'Change ownership: `chown user:group <path>`',
                    'Run with elevated privileges if appropriate'
                ]
            ),
            'eacces': ErrorAnalysis(
                error_type='Permission Error',
                severity='MEDIUM',
                explanation='Access denied: permission was denied for this operation. '
                           'The file or resource permissions prevent access by the current user.',
                root_cause='File or resource permissions prevent access.',
                suggestions=[
                    'Change permissions: `chmod` or `chown`',
                    'Check file ownership: `ls -la <path>`',
                    'Run with elevated privileges if appropriate'
                ]
            ),
            
            # Memory errors - include memory, heap, allocation, javascript
            'heap out of memory': ErrorAnalysis(
                error_type='Memory Error',
                severity='CRITICAL',
                explanation='JavaScript heap memory allocation failed. '
                           'The Node.js application exceeded its memory limit. '
                           'This is often caused by a memory leak or insufficient heap allocation.',
                root_cause='Memory leak or insufficient heap allocation.',
                suggestions=[
                    'Increase heap size: `node --max-old-space-size=4096 app.js`',
                    'Profile memory usage to find leaks',
                    'Optimize memory-intensive operations'
                ]
            ),
            
            # Python errors - include module, import, pip, installed
            'modulenotfounderror': ErrorAnalysis(
                error_type='Import Error',
                severity='HIGH',
                explanation='A Python import failed: the required module is not installed. '
                           'The module could not be found in your Python environment.',
                root_cause='The module is not in the current Python environment.',
                suggestions=[
                    'Install the module: `pip install <module_name>`',
                    'Check requirements.txt and run: `pip install -r requirements.txt`',
                    'Verify virtual environment is activated'
                ]
            ),
            'no module named': ErrorAnalysis(
                error_type='Import Error',
                severity='HIGH',
                explanation='Python import error: cannot find the specified module. '
                           'The module is not installed or not in the Python path.',
                root_cause='The module is not installed or not in the Python path.',
                suggestions=[
                    'Install the module: `pip install <module_name>`',
                    'Check your PYTHONPATH',
                    'Verify the module name is correct'
                ]
            ),
            # Key error - include dictionary, key, exist, access
            'keyerror': ErrorAnalysis(
                error_type='Key Error',
                severity='MEDIUM',
                explanation='Dictionary key error: the specified key does not exist. '
                           'Attempted to access a dictionary key that was not found.',
                root_cause='The key does not exist in the dictionary.',
                suggestions=[
                    'Use `.get(key, default)` instead of direct access',
                    'Check if key exists: `if key in dict:`',
                    'Print dictionary keys to debug: `print(dict.keys())`'
                ]
            ),
            # Database error - include table, database, schema, migrations
            'no such table': ErrorAnalysis(
                error_type='Database Error',
                severity='CRITICAL',
                explanation='Database schema error: the specified table does not exist. '
                           'The database is missing required tables. '
                           'Run migrations to create the schema.',
                root_cause='Migrations have not been run.',
                suggestions=[
                    'Run migrations: `python manage.py migrate`',
                    'Create migrations: `python manage.py makemigrations`',
                    'Check database initialization'
                ]
            ),
            
            # Go errors - include nil, pointer, memory, panic
            'nil pointer': ErrorAnalysis(
                error_type='Nil Pointer',
                severity='CRITICAL',
                explanation='Nil pointer dereference caused a panic. '
                           'Attempted to access memory through a nil (null) pointer. '
                           'This is a critical error that crashes the program.',
                root_cause='Pointer was not initialized or is nil.',
                suggestions=[
                    'Check for nil before use: `if ptr != nil`',
                    'Initialize pointers properly',
                    'Use error returns instead of nil pointers'
                ]
            ),
            # Go errors - include deadlock, goroutine, blocked, waiting, channel
            'deadlock': ErrorAnalysis(
                error_type='Deadlock',
                severity='CRITICAL',
                explanation='Goroutine deadlock detected. All goroutines are blocked and waiting. '
                           'No goroutine can make progress because they are waiting on each other.',
                root_cause='Circular dependency in channel or mutex operations.',
                suggestions=[
                    'Use buffered channels: `ch := make(chan int, 1)`',
                    'Add timeouts to channel operations',
                    'Review goroutine blocking patterns'
                ]
            ),
        }
    
    def _make_cache_key(self, error_message: str) -> str:
        """Create cache key from error message."""
        # Normalize error message for caching
        return error_message.strip().lower()[:100]
