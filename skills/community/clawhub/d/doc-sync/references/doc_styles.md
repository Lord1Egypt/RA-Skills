# Documentation Styles

This reference defines the required documentation styles for Python and Go projects.

## Python (Google Style)

Use the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) for all Python docstrings.

### Function Example
```python
def function_with_types_in_docstring(param1, param2):
    """Example function with types documented in the docstring.

    Args:
        param1 (int): The first parameter.
        param2 (str): The second parameter.

    Returns:
        bool: The return value. True for success, False otherwise.
    """
    return True
```

### Class Example
```python
class ExampleClass:
    """The summary line for a class docstring should be on one line.

    Attributes:
        attr1 (str): Description of `attr1`.
        attr2 (int): Description of `attr2`.
    """
    def __init__(self, attr1, attr2):
        self.attr1 = attr1
        self.attr2 = attr2
```

## Go (Standard Style)

Follow [Effective Go](https://golang.org/doc/effective_go.html#commentary) and [Go Doc Comments](https://go.dev/doc/comment).

### Function Example
```go
// ExportedFunction performs a specific task.
// It returns an error if something goes wrong.
func ExportedFunction(param1 int) error {
    return nil
}
```

### Package Example
```go
// Package example provides functionality for demonstrating Go doc comments.
package example
```

### Struct Example
```go
// ExampleStruct represents a data structure.
type ExampleStruct struct {
    // Field1 is the first field.
    Field1 string
}
```
