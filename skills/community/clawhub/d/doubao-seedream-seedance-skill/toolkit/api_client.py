"""
API client for Volcengine services.

Provides HTTP client with authentication, error handling, and retry logic.
"""

from typing import Optional, Dict, Any
import httpx
from toolkit.config import ConfigManager
from toolkit.error_handler import (
    VolcengineError,
    AuthenticationError,
    APIError,
    NetworkError,
    handle_api_error
)


class VolcengineAPIClient:
    """
    HTTP client for Volcengine API with built-in error handling.
    
    Features:
    - Bearer token authentication
    - Automatic retry on transient failures
    - Request/response logging
    - Error transformation to user-friendly messages
    """
    
    def __init__(self, config: Optional[ConfigManager] = None):
        """
        Initialize API client.
        
        Args:
            config: Configuration manager (creates default if None)
        """
        self.config = config or ConfigManager()
        self.base_url = self.config.get_base_url()
        self.timeout = self.config.get_timeout()
        self.max_retries = self.config.get("max_retries", 3)
        
        # Validate API key
        self.api_key = self.config.get_api_key()
        if not self.api_key:
            raise AuthenticationError(
                message="API key not configured",
                context={"hint": "Set ARK_API_KEY environment variable or configure in .volcengine/config.yaml"}
            )
        
        # Create HTTP client
        self.client = httpx.Client(
            base_url=self.base_url,
            timeout=self.timeout,
            headers=self._get_headers()
        )
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with authentication."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "VolcengineAPISkill/1.0"
        }
    
    def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Make HTTP request with error handling.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            **kwargs: Additional request parameters
            
        Returns:
            Response data as dictionary
            
        Raises:
            VolcengineError: On API or network errors
        """
        retries = 0
        last_error = None
        
        while retries <= self.max_retries:
            try:
                response = self.client.request(method, endpoint, **kwargs)
                
                # Check for HTTP errors
                if response.status_code >= 400:
                    error_data = response.json() if response.content else {}
                    error_msg = error_data.get("message", f"HTTP {response.status_code}")
                    
                    if response.status_code in (401, 403):
                        raise AuthenticationError(
                            message=error_msg,
                            context={"status_code": response.status_code}
                        )
                    else:
                        raise APIError(
                            message=error_msg,
                            status_code=response.status_code,
                            context=error_data
                        )
                
                return response.json()
                
            except httpx.TimeoutException as e:
                last_error = NetworkError(
                    message="Request timeout",
                    original_error=str(e)
                )
                retries += 1
                
            except httpx.NetworkError as e:
                last_error = NetworkError(
                    message="Network connection failed",
                    original_error=str(e)
                )
                retries += 1
                
            except VolcengineError:
                raise
                
            except Exception as e:
                raise handle_api_error(e)
        
        # All retries exhausted
        raise last_error or NetworkError(message="Request failed after retries")
    
    def get(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make GET request."""
        return self._request("GET", endpoint, **kwargs)
    
    def post(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make POST request."""
        return self._request("POST", endpoint, **kwargs)
    
    def put(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make PUT request."""
        return self._request("PUT", endpoint, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make DELETE request."""
        return self._request("DELETE", endpoint, **kwargs)
    
    def close(self) -> None:
        """Close HTTP client."""
        self.client.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
