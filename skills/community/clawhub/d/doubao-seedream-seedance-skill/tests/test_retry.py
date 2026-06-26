"""
Tests for retry utilities.

Tests verify retry logic and backoff behavior.
"""

import pytest
import time
from toolkit.utils.retry import RetryConfig, retry_with_backoff


class TestRetryConfig:
    """Test cases for RetryConfig."""
    
    def test_default_config(self):
        """Test default configuration."""
        config = RetryConfig()
        
        assert config.max_attempts == 3
        assert config.base_delay == 1.0
        assert config.max_delay == 60.0
        assert config.exponential_base == 2.0
        assert config.jitter is True
    
    def test_custom_config(self):
        """Test custom configuration."""
        config = RetryConfig(
            max_attempts=5,
            base_delay=2.0,
            max_delay=120.0
        )
        
        assert config.max_attempts == 5
        assert config.base_delay == 2.0
        assert config.max_delay == 120.0
    
    def test_get_delay_first_attempt(self):
        """Test delay for first attempt."""
        config = RetryConfig(base_delay=1.0, jitter=False)
        
        delay = config.get_delay(0)
        assert delay == 1.0
    
    def test_get_delay_second_attempt(self):
        """Test delay for second attempt."""
        config = RetryConfig(base_delay=1.0, exponential_base=2.0, jitter=False)
        
        delay = config.get_delay(1)
        assert delay == 2.0
    
    def test_get_delay_third_attempt(self):
        """Test delay for third attempt."""
        config = RetryConfig(base_delay=1.0, exponential_base=2.0, jitter=False)
        
        delay = config.get_delay(2)
        assert delay == 4.0
    
    def test_get_delay_max_delay(self):
        """Test delay respects max_delay."""
        config = RetryConfig(base_delay=10.0, max_delay=15.0, jitter=False)
        
        delay = config.get_delay(2)  # Would be 40 without max
        assert delay == 15.0
    
    def test_get_delay_with_jitter(self):
        """Test delay includes jitter."""
        config = RetryConfig(base_delay=1.0, jitter=True)
        
        delays = [config.get_delay(0) for _ in range(10)]
        
        # All delays should be different due to jitter
        assert len(set(delays)) > 1
        
        # All delays should be within expected range (0.5x to 1.5x base)
        for delay in delays:
            assert 0.5 <= delay <= 1.5


class TestRetryWithBackoff:
    """Test cases for retry_with_backoff decorator."""
    
    def test_success_no_retry(self):
        """Test successful function doesn't retry."""
        call_count = 0
        
        @retry_with_backoff()
        def successful_func():
            nonlocal call_count
            call_count += 1
            return "success"
        
        result = successful_func()
        
        assert result == "success"
        assert call_count == 1
    
    def test_retry_on_exception(self):
        """Test retry on exception."""
        call_count = 0
        
        @retry_with_backoff(config=RetryConfig(max_attempts=3, base_delay=0.01))
        def failing_func():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("Not yet")
            return "success"
        
        result = failing_func()
        
        assert result == "success"
        assert call_count == 3
    
    def test_max_attempts_exceeded(self):
        """Test max attempts exceeded raises exception."""
        call_count = 0
        
        @retry_with_backoff(config=RetryConfig(max_attempts=2, base_delay=0.01))
        def always_failing():
            nonlocal call_count
            call_count += 1
            raise ValueError("Always fails")
        
        with pytest.raises(ValueError):
            always_failing()
        
        assert call_count == 2
    
    def test_specific_exception_only(self):
        """Test retry only on specific exceptions."""
        call_count = 0
        
        @retry_with_backoff(
            config=RetryConfig(max_attempts=3, base_delay=0.01),
            exceptions=ValueError
        )
        def mixed_errors():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise ValueError("Retry this")
            raise TypeError("Don't retry this")
        
        with pytest.raises(TypeError):
            mixed_errors()
        
        assert call_count == 2
    
    def test_preserves_function_metadata(self):
        """Test decorator preserves function metadata."""
        @retry_with_backoff()
        def my_func():
            """My docstring."""
            pass
        
        assert my_func.__name__ == "my_func"
        assert my_func.__doc__ == "My docstring."
