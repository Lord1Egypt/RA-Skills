"""
Tests for API client.

Tests verify HTTP requests, authentication, and error handling.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import httpx
from toolkit.api_client import VolcengineAPIClient
from toolkit.config import ConfigManager
from toolkit.error_handler import AuthenticationError, APIError, NetworkError


class TestVolcengineAPIClient:
    """Test cases for VolcengineAPIClient."""
    
    def test_initialization_with_config(self):
        """Test client initialization with config."""
        config = ConfigManager()
        config.set("api_key", "test-api-key")
        
        client = VolcengineAPIClient(config=config)
        assert client.api_key == "test-api-key"
        assert client.base_url == config.get_base_url()
        client.close()
    
    def test_initialization_without_api_key(self):
        """Test that initialization fails without API key."""
        config = ConfigManager()
        config.set("api_key", None)
        
        with pytest.raises(AuthenticationError):
            VolcengineAPIClient(config=config)
    
    def test_get_headers(self):
        """Test header generation."""
        config = ConfigManager()
        config.set("api_key", "test-key")
        
        client = VolcengineAPIClient(config=config)
        headers = client._get_headers()
        
        assert headers["Authorization"] == "Bearer test-key"
        assert headers["Content-Type"] == "application/json"
        client.close()
    
    @patch('httpx.Client.request')
    def test_successful_get_request(self, mock_request):
        """Test successful GET request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "test"}
        mock_request.return_value = mock_response
        
        config = ConfigManager()
        config.set("api_key", "test-key")
        
        client = VolcengineAPIClient(config=config)
        result = client.get("/test/endpoint")
        
        assert result == {"data": "test"}
        mock_request.assert_called_once_with("GET", "/test/endpoint")
        client.close()
    
    @patch('httpx.Client.request')
    def test_successful_post_request(self, mock_request):
        """Test successful POST request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "123"}
        mock_request.return_value = mock_response
        
        config = ConfigManager()
        config.set("api_key", "test-key")
        
        client = VolcengineAPIClient(config=config)
        result = client.post("/test/endpoint", json={"key": "value"})
        
        assert result == {"id": "123"}
        mock_request.assert_called_once_with("POST", "/test/endpoint", json={"key": "value"})
        client.close()
    
    @patch('httpx.Client.request')
    def test_authentication_error_401(self, mock_request):
        """Test authentication error on 401."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.content = b'{"message": "Unauthorized"}'
        mock_response.json.return_value = {"message": "Unauthorized"}
        mock_request.return_value = mock_response
        
        config = ConfigManager()
        config.set("api_key", "test-key")
        
        client = VolcengineAPIClient(config=config)
        
        with pytest.raises(AuthenticationError):
            client.get("/test/endpoint")
        
        client.close()
    
    @patch('httpx.Client.request')
    def test_authentication_error_403(self, mock_request):
        """Test authentication error on 403."""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.content = b'{"message": "Forbidden"}'
        mock_response.json.return_value = {"message": "Forbidden"}
        mock_request.return_value = mock_response
        
        config = ConfigManager()
        config.set("api_key", "test-key")
        
        client = VolcengineAPIClient(config=config)
        
        with pytest.raises(AuthenticationError):
            client.get("/test/endpoint")
        
        client.close()
    
    @patch('httpx.Client.request')
    def test_api_error_500(self, mock_request):
        """Test API error on 500."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.content = b'{"message": "Internal Server Error"}'
        mock_response.json.return_value = {"message": "Internal Server Error"}
        mock_request.return_value = mock_response
        
        config = ConfigManager()
        config.set("api_key", "test-key")
        
        client = VolcengineAPIClient(config=config)
        
        with pytest.raises(APIError) as exc_info:
            client.get("/test/endpoint")
        
        assert exc_info.value.status_code == 500
        client.close()
    
    @patch('httpx.Client.request')
    def test_network_error_retry(self, mock_request):
        """Test retry on network error."""
        # First two calls fail, third succeeds
        mock_request.side_effect = [
            httpx.NetworkError("Connection failed"),
            httpx.NetworkError("Connection failed"),
            Mock(status_code=200, json=lambda: {"data": "success"})
        ]
        
        config = ConfigManager()
        config.set("api_key", "test-key")
        config.set("max_retries", 3)
        
        client = VolcengineAPIClient(config=config)
        result = client.get("/test/endpoint")
        
        assert result == {"data": "success"}
        assert mock_request.call_count == 3
        client.close()
    
    @patch('httpx.Client.request')
    def test_timeout_retry(self, mock_request):
        """Test retry on timeout."""
        mock_request.side_effect = [
            httpx.TimeoutException("Request timeout"),
            Mock(status_code=200, json=lambda: {"data": "success"})
        ]
        
        config = ConfigManager()
        config.set("api_key", "test-key")
        config.set("max_retries", 3)
        
        client = VolcengineAPIClient(config=config)
        result = client.get("/test/endpoint")
        
        assert result == {"data": "success"}
        assert mock_request.call_count == 2
        client.close()
    
    @patch('httpx.Client.request')
    def test_max_retries_exceeded(self, mock_request):
        """Test failure after max retries."""
        mock_request.side_effect = httpx.NetworkError("Connection failed")
        
        config = ConfigManager()
        config.set("api_key", "test-key")
        config.set("max_retries", 2)
        
        client = VolcengineAPIClient(config=config)
        
        with pytest.raises(NetworkError):
            client.get("/test/endpoint")
        
        assert mock_request.call_count == 3  # Initial + 2 retries
        client.close()
    
    def test_context_manager(self):
        """Test context manager usage."""
        config = ConfigManager()
        config.set("api_key", "test-key")
        
        with VolcengineAPIClient(config=config) as client:
            assert client.api_key == "test-key"
    
    @patch('httpx.Client.request')
    def test_put_request(self, mock_request):
        """Test PUT request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"updated": True}
        mock_request.return_value = mock_response
        
        config = ConfigManager()
        config.set("api_key", "test-key")
        
        client = VolcengineAPIClient(config=config)
        result = client.put("/test/endpoint", json={"key": "new-value"})
        
        assert result == {"updated": True}
        client.close()
    
    @patch('httpx.Client.request')
    def test_delete_request(self, mock_request):
        """Test DELETE request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"deleted": True}
        mock_request.return_value = mock_response
        
        config = ConfigManager()
        config.set("api_key", "test-key")
        
        client = VolcengineAPIClient(config=config)
        result = client.delete("/test/endpoint")
        
        assert result == {"deleted": True}
        client.close()
