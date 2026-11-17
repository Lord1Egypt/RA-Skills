# Go TDD Best Practices

## Test Framework: testing (standard library)

### Setup

```bash
# Run tests
go test ./...           # All tests
go test -v ./...        # Verbose
go test -run TestName   # Single test
go test -cover          # With coverage
```

### Test Structure (Table-Driven Tests)

```go
// mymodule_test.go
package mymodule

import "testing"

func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive numbers", 1, 2, 3},
        {"negative numbers", -1, -2, -3},
        {"zero", 0, 0, 0},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := Add(tt.a, tt.b)
            if result != tt.expected {
                t.Errorf("Add(%d, %d) = %d, want %d", tt.a, tt.b, result, tt.expected)
            }
        })
    }
}

func TestDivide(t *testing.T) {
    tests := []struct {
        name      string
        a, b      int
        expected  int
        wantError bool
    }{
        {"valid division", 6, 2, 3, false},
        {"division by zero", 1, 0, 0, true},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result, err := Divide(tt.a, tt.b)
            if tt.wantError && err == nil {
                t.Error("expected error, got nil")
            }
            if !tt.wantError && result != tt.expected {
                t.Errorf("Divide(%d, %d) = %d, want %d", tt.a, tt.b, result, tt.expected)
            }
        })
    }
}
```

### Mocking

```go
// Use interfaces for mocking
type Service interface {
    Fetch(id string) (Data, error)
}

// In production code
type RealService struct{}
func (r *RealService) Fetch(id string) (Data, error) { ... }

// In test code
type MockService struct{}
func (m *MockService) Fetch(id string) (Data, error) {
    return Data{ID: id}, nil
}

// Or use testify/mock
// go get github.com/stretchr/testify/mock
```

## Best Practices

- Always use table-driven tests
- Test file: `same_file_test.go` in same package
- Use `t.Run()` for subtests (better organization)
- Mock via interfaces (not monkey-patching)
- Error format: `t.Errorf("got %v, want %v", got, want)`
- Benchmark tests: `func BenchmarkX(b *testing.B)`
