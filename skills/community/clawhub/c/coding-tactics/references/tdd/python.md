# Python TDD Best Practices

## Test Framework: pytest

### Setup

```bash
# Install
pip install pytest pytest-mock

# Run tests
pytest              # Run all tests
pytest -v           # Verbose
pytest --tb=short   # Short traceback
pytest -x           # Stop on first failure
```

### Test Structure

```python
# test_<module>.py
import pytest
from unittest.mock import Mock, patch
from mymodule import MyClass

class TestMyClass:
    """Test suite for MyClass."""

    def test_initialization(self):
        """Test object initialization."""
        obj = MyClass(param="value")
        assert obj.param == "value"

    def test_method_returns_expected(self):
        """Test method returns correct result."""
        obj = MyClass()
        result = obj.method(input_data)
        assert result == expected_output

    def test_method_raises_on_invalid_input(self):
        """Test method raises appropriate exception."""
        obj = MyClass()
        with pytest.raises(ValueError, match="invalid input"):
            obj.method(None)

    @patch("mymodule.external_dependency")
    def test_with_mock(self, mock_dep):
        """Test with mocked dependency."""
        mock_dep.return_value = "mocked"
        obj = MyClass()
        result = obj.method_using_dep()
        assert result == "mocked"
```

### Mocking

```python
# Use pytest-mock fixture
def test_with_mocker(mocker):
    mock_service = mocker.patch("mymodule.Service")
    mock_service.return_value.fetch.return_value = {"data": 1}

# Use unittest.mock
from unittest.mock import Mock, MagicMock, patch
```

## Best Practices

- One assert per test (prefer single concept per test)
- Test names: `test_<method>_<scenario>_<expected>`
- Use fixtures for setup: `@pytest.fixture`
- Parametrize: `@pytest.mark.parametrize`
- Keep tests fast (< 100ms each)
- No test logic (no if/else in tests)
