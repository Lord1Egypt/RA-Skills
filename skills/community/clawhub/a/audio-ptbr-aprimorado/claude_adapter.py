#!/usr/bin/env python3
"""Claude Adapter - Intelligent audio responses with proper CLI interface."""
import sys
import os
import json
import logging
import subprocess
from typing import Optional, Dict
from pathlib import Path

# Configure logging
logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'WARNING'))
logger = logging.getLogger(__name__)

# Try to import Claude SDK
try:
    from anthropic import Anthropic
    CLAUDE_AVAILABLE = True
except ImportError:
    CLAUDE_AVAILABLE = False

class ClaudeResponseError(Exception):
    """Exception for Claude API errors."""
    pass

class AgentResponseError(Exception):
    """Exception for OpenClaw agent errors."""
    pass

class AudioResponseGenerator:
    """Generate intelligent responses for audio input."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize response generator.
        
        Args:
            api_key: Anthropic API key (optional, auto-detected from env)
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.claude_available = CLAUDE_AVAILABLE and self.api_key is not None
        self.timeout = int(os.environ.get("RESPONSE_TIMEOUT", "30"))
        
    def get_claude_response(self, transcript: str) -> str:
        """
        Get intelligent response from Claude using API.
        
        Args:
            transcript: User's transcribed message
            
        Returns:
            Response text suitable for TTS (short, natural)
            
        Raises:
            ClaudeResponseError: If Claude API fails
        """
        if not self.claude_available:
            raise ClaudeResponseError("Claude SDK not available or no API key")
        
        try:
            client = Anthropic(api_key=self.api_key)
            
            # System prompt optimized for voice interaction
            system_prompt = """Você é um assistente de voz amigável em português brasileiro.

Regras importantes:
- Respostas curtas e diretas (máx 2-3 frases)
- Linguagem natural e coloquial (como falaria um amigo)
- Sem formatação, sem listas, sem emojis
- Sem explicações longas
- Se não souber, diga honestamente
- Tone caloroso e conversacional"""
            
            # Call API with timeout
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",  # Updated to a valid and high-performance model
                max_tokens=256,
                timeout=self.timeout,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": transcript}
                ]
            )
            
            response = message.content[0].text.strip()
            
            if not response:
                raise ClaudeResponseError("Empty response from Claude")
            
            return response
            
        except TimeoutError as e:
            raise ClaudeResponseError(f"Claude API timeout after {self.timeout}s")
        except Exception as e:
            raise ClaudeResponseError(f"Claude API error: {str(e)}")
    
    def get_agent_response(self, transcript: str) -> str:
        """
        Get response from OpenClaw agent (fallback).
        
        Args:
            transcript: User's transcribed message
            
        Returns:
            Response text
            
        Raises:
            AgentResponseError: If agent fails
        """
        try:
            # FIXED: Corrected openclaw CLI command for agent inference
            result = subprocess.run(
                ["openclaw", "infer", "model", "run", "--prompt", transcript, "--json"],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            if result.returncode != 0:
                raise AgentResponseError(f"Agent returned {result.returncode}")
            
            try:
                data = json.loads(result.stdout)
                response = data.get("response", "").strip()
                
                if not response:
                    raise AgentResponseError("Empty agent response")
                
                return response
                
            except json.JSONDecodeError:
                # Fallback: treat stdout as response
                response = result.stdout.strip()
                if response:
                    return response
                raise AgentResponseError("Invalid JSON from agent")
                
        except TimeoutError:
            raise AgentResponseError(f"Agent timeout after {self.timeout}s")
        except FileNotFoundError:
            raise AgentResponseError("openclaw command not found")
        except Exception as e:
            raise AgentResponseError(f"Agent error: {str(e)}")
    
    def generate_response(self, transcript: str, use_claude: bool = True) -> str:
        """
        Generate intelligent response with fallback chain.
        
        Args:
            transcript: User's transcribed message
            use_claude: Try Claude first if available
            
        Returns:
            Response text suitable for TTS
            
        Raises:
            ValueError: If transcript is empty
        """
        if not transcript or not transcript.strip():
            raise ValueError("Transcript cannot be empty")
        
        errors = []
        
        # Try Claude first
        if use_claude and self.claude_available:
            try:
                response = self.get_claude_response(transcript)
                logger.info("Got response from Claude")
                return response
            except ClaudeResponseError as e:
                logger.warning(f"Claude failed: {e}")
                errors.append(f"Claude: {str(e)}")
        
        # Try OpenClaw agent
        try:
            response = self.get_agent_response(transcript)
            logger.info("Got response from OpenClaw agent")
            return response
        except AgentResponseError as e:
            logger.warning(f"Agent failed: {e}")
            errors.append(f"Agent: {str(e)}")
        
        # Final fallback: simple echo
        logger.warning(f"All methods failed: {errors}")
        return f"Entendi: {transcript}. Como posso ajudar?"


def parse_args():
    """Parse command-line arguments."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Generate intelligent responses for audio transcripts',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Qual é a capital da França?"
  %(prog)s --text "Olá" --claude-only
  %(prog)s --json "pergunta" 
  
Environment variables:
  ANTHROPIC_API_KEY    Claude API key (for Claude responses)
  RESPONSE_TIMEOUT     Timeout in seconds (default: 30)
  LOG_LEVEL           Logging level: DEBUG, INFO, WARNING, ERROR (default: WARNING)
        """
    )
    
    parser.add_argument(
        'transcript',
        help='Transcribed text to process'
    )
    
    parser.add_argument(
        '--claude-only',
        action='store_true',
        help='Only use Claude, no OpenClaw agent fallback'
    )
    
    parser.add_argument(
        '--agent-only',
        action='store_true',
        help='Only use OpenClaw agent, no Claude'
    )
    
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output result as JSON (for integration)'
    )
    
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    return parser.parse_args()


def main():
    """Main CLI entry point."""
    try:
        args = parse_args()
        
        # Configure logging
        if args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        
        # Generate response
        generator = AudioResponseGenerator()
        
        use_claude = not args.agent_only
        response = generator.generate_response(args.transcript, use_claude=use_claude)
        
        # Output
        if args.json:
            result = {
                "success": True,
                "response": response,
                "transcript": args.transcript,
            }
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(response)
        
        return 0
        
    except ValueError as e:
        error_msg = f"Invalid input: {str(e)}"
        logger.error(error_msg)
        
        if args.json if 'args' in locals() else False:
            print(json.dumps({"success": False, "error": error_msg}, ensure_ascii=False))
        else:
            print(f"Error: {error_msg}", file=sys.stderr)
        
        return 1
        
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg, exc_info=True)
        
        if args.json if 'args' in locals() else False:
            print(json.dumps({"success": False, "error": error_msg}, ensure_ascii=False))
        else:
            print(f"Error: {error_msg}", file=sys.stderr)
        
        return 1


if __name__ == "__main__":
    sys.exit(main())
