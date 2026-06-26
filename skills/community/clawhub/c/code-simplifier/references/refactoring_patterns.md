# Refactoring Patterns

Detailed refactoring techniques and patterns used by the code-simplifier skill.

## Table of Contents
1. [Structural Patterns](#structural-patterns)
2. [Conditional Simplification](#conditional-simplification)
3. [Loop Optimization](#loop-optimization)
4. [Error Handling Patterns](#error-handling-patterns)
5. [Code Extraction Patterns](#code-extraction-patterns)
6. [Naming Improvement Patterns](#naming-improvement-patterns)
7. [Type Safety Patterns](#type-safety-patterns)
8. [Async/Await Patterns](#asyncawait-patterns)
9. [Class and Object Patterns](#class-and-object-patterns)
10. [Functional Patterns](#functional-patterns)

## Structural Patterns

### Pattern 1: Early Return
**Problem**: Deeply nested code with multiple exit points
**Solution**: Use early returns to flatten structure

**Before**:
```python
def process_item(item):
    if item is not None:
        if 'data' in item:
            data = item['data']
            if isinstance(data, dict):
                if 'value' in data:
                    # Process value
                    return result
                else:
                    return None
            else:
                return None
        else:
            return None
    else:
        return None
```

**After**:
```python
def process_item(item):
    if item is None:
        return None
    if 'data' not in item:
        return None
    
    data = item['data']
    if not isinstance(data, dict):
        return None
    if 'value' not in data:
        return None
    
    # Process value
    return result
```

### Pattern 2: Guard Clauses
**Problem**: Complex preconditions mixed with main logic
**Solution**: Separate validation from processing

**Before**:
```javascript
function calculateTotal(items) {
    let total = 0;
    if (items && Array.isArray(items)) {
        for (let item of items) {
            if (item && item.price && item.quantity) {
                total += item.price * item.quantity;
            }
        }
    }
    return total;
}
```

**After**:
```javascript
function calculateTotal(items) {
    if (!items || !Array.isArray(items)) {
        return 0;
    }
    
    let total = 0;
    for (let item of items) {
        if (!item || !item.price || !item.quantity) {
            continue;
        }
        total += item.price * item.quantity;
    }
    return total;
}
```

### Pattern 3: Decomposition
**Problem**: Long functions doing multiple things
**Solution**: Break into smaller, focused functions

**Before**:
```python
def process_order(order):
    # Validate order
    if not order or 'items' not in order:
        raise ValueError("Invalid order")
    
    # Calculate total
    total = 0
    for item in order['items']:
        total += item['price'] * item['quantity']
    
    # Apply discount
    if order.get('discount'):
        total *= (1 - order['discount'])
    
    # Update inventory
    for item in order['items']:
        inventory[item['id']] -= item['quantity']
    
    # Create receipt
    receipt = {
        'order_id': order['id'],
        'total': total,
        'items': order['items']
    }
    
    return receipt
```

**After**:
```python
def process_order(order):
    _validate_order(order)
    total = _calculate_total(order)
    total = _apply_discount(order, total)
    _update_inventory(order)
    return _create_receipt(order, total)

def _validate_order(order):
    if not order or 'items' not in order:
        raise ValueError("Invalid order")

def _calculate_total(order):
    return sum(item['price'] * item['quantity'] for item in order['items'])

def _apply_discount(order, total):
    if order.get('discount'):
        return total * (1 - order['discount'])
    return total

def _update_inventory(order):
    for item in order['items']:
        inventory[item['id']] -= item['quantity']

def _create_receipt(order, total):
    return {
        'order_id': order['id'],
        'total': total,
        'items': order['items']
    }
```

## Conditional Simplification

### Pattern 4: Boolean Expression Simplification
**Problem**: Complex boolean expressions
**Solution**: Apply boolean algebra rules

**Before**:
```python
if (x > 0 and y > 0) or (x > 0 and z > 0):
    # Do something
```

**After**:
```python
if x > 0 and (y > 0 or z > 0):
    # Do something
```

### Pattern 5: Switch/Case Pattern
**Problem**: Long if-else chains
**Solution**: Use dictionary dispatch or switch statements

**Before**:
```python
def handle_command(command):
    if command == 'start':
        start_process()
    elif command == 'stop':
        stop_process()
    elif command == 'restart':
        restart_process()
    elif command == 'status':
        get_status()
    else:
        raise ValueError(f"Unknown command: {command}")
```

**After**:
```python
def handle_command(command):
    handlers = {
        'start': start_process,
        'stop': stop_process,
        'restart': restart_process,
        'status': get_status
    }
    
    handler = handlers.get(command)
    if not handler:
        raise ValueError(f"Unknown command: {command}")
    
    return handler()
```

### Pattern 6: Null Object Pattern
**Problem**: Frequent null checks
**Solution**: Use default objects

**Before**:
```python
class User:
    def __init__(self, name):
        self.name = name
    
    def get_preferences(self):
        return self.preferences if hasattr(self, 'preferences') else None

user = get_user()
prefs = user.get_preferences() if user else None
theme = prefs.theme if prefs else 'default'
```

**After**:
```python
class NullPreferences:
    theme = 'default'
    language = 'en'
    notifications = False

class User:
    def __init__(self, name, preferences=None):
        self.name = name
        self.preferences = preferences or NullPreferences()
    
    def get_preferences(self):
        return self.preferences

user = get_user() or NullUser()
theme = user.get_preferences().theme
```

## Loop Optimization

### Pattern 7: Loop Unrolling
**Problem**: Simple loops with predictable patterns
**Solution**: Manual unrolling for performance

**Before**:
```python
total = 0
for i in range(len(data)):
    total += data[i]
```

**After** (for performance-critical code):
```python
total = 0
i = 0
while i + 3 < len(data):
    total += data[i] + data[i+1] + data[i+2] + data[i+3]
    i += 4
while i < len(data):
    total += data[i]
    i += 1
```

### Pattern 8: Loop Fusion
**Problem**: Multiple loops over same data
**Solution**: Combine loops

**Before**:
```python
names = []
for user in users:
    names.append(user.name)

ages = []
for user in users:
    ages.append(user.age)
```

**After**:
```python
names = []
ages = []
for user in users:
    names.append(user.name)
    ages.append(user.age)
```

### Pattern 9: Loop to Comprehension
**Problem**: Simple transformation loops
**Solution**: Use list/dict comprehensions

**Before**:
```python
squares = []
for x in range(10):
    squares.append(x * x)
```

**After**:
```python
squares = [x * x for x in range(10)]
```

## Error Handling Patterns

### Pattern 10: Centralized Error Handling
**Problem**: Duplicate error handling code
**Solution**: Extract error handling logic

**Before**:
```python
def process_file(filename):
    try:
        with open(filename, 'r') as f:
            data = f.read()
        return parse_data(data)
    except FileNotFoundError:
        logger.error(f"File not found: {filename}")
        return None
    except PermissionError:
        logger.error(f"Permission denied: {filename}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None

def download_file(url):
    try:
        response = requests.get(url)
        return response.content
    except requests.RequestException as e:
        logger.error(f"Download failed: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None
```

**After**:
```python
def handle_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            logger.error(f"File not found: {e.filename}")
            return None
        except PermissionError as e:
            logger.error(f"Permission denied: {e.filename}")
            return None
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None
    return wrapper

@handle_errors
def process_file(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return parse_data(data)

@handle_errors
def download_file(url):
    response = requests.get(url)
    return response.content
```

### Pattern 11: Result Object Pattern
**Problem**: Functions returning success/failure with data
**Solution**: Use result objects

**Before**:
```python
def process_data(data):
    if not data:
        return None, "No data provided"
    
    try:
        result = complex_processing(data)
        return result, None
    except Exception as e:
        return None, str(e)

result, error = process_data(input_data)
if error:
    handle_error(error)
else:
    use_result(result)
```

**After**:
```python
from dataclasses import dataclass
from typing import Generic, TypeVar, Optional

T = TypeVar('T')

@dataclass
class Result(Generic[T]):
    value: Optional[T] = None
    error: Optional[str] = None
    
    @property
    def is_success(self):
        return self.error is None
    
    @property
    def is_failure(self):
        return self.error is not None

def process_data(data) -> Result:
    if not data:
        return Result(error="No data provided")
    
    try:
        result = complex_processing(data)
        return Result(value=result)
    except Exception as e:
        return Result(error=str(e))

result = process_data(input_data)
if result.is_failure:
    handle_error(result.error)
else:
    use_result(result.value)
```

## Code Extraction Patterns

### Pattern 12: Extract Method
**Problem**: Code blocks that can be named
**Solution**: Extract to separate method

**Before**:
```python
def generate_report(data):
    # Calculate statistics
    total = sum(item['value'] for item in data)
    average = total / len(data) if data else 0
    max_value = max(item['value'] for item in data) if data else 0
    
    # Format report
    report = f"Total: {total}\n"
    report += f"Average: {average:.2f}\n"
    report += f"Max: {max_value}\n"
    
    return report
```

**After**:
```python
def generate_report(data):
    stats = _calculate_statistics(data)
    return _format_report(stats)

def _calculate_statistics(data):
    if not data:
        return {'total': 0, 'average': 0, 'max': 0}
    
    total = sum(item['value'] for item in data)
    average = total / len(data)
    max_value = max(item['value'] for item in data)
    
    return {'total': total, 'average': average, 'max': max_value}

def _format_report(stats):
    return f"""Total: {stats['total']}
Average: {stats['average']:.2f}
Max: {stats['max']}"""
```

### Pattern 13: Extract Class
**Problem**: Groups of related functions
**Solution**: Extract to class

**Before**:
```python
# Multiple related functions
def create_user(name, email):
    # validation logic
    pass

def update_user(user_id, updates):
    # update logic
    pass

def delete_user(user_id):
    # deletion logic
    pass

def get_user(user_id):
    # retrieval logic
    pass
```

**After**:
```python
class UserService:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def create(self, name, email):
        # validation and creation logic
        pass
    
    def update(self, user_id, updates):
        # update logic
        pass
    
    def delete(self, user_id):
        # deletion logic
        pass
    
    def get(self, user_id):
        # retrieval logic
        pass
```

## Naming Improvement Patterns

### Pattern 14: Intent-Revealing Names
**Problem**: Unclear variable/function names
**Solution**: Use names that reveal intent

**Before**:
```python
def proc(d):
    r = []
    for i in d:
        if i > 0:
            r.append(i * 2)
    return r
```

**After**:
```python
def filter_and_double_positive_numbers(numbers):
    doubled_positives = []
    for number in numbers:
        if number > 0:
            doubled_positives.append(number * 2)
    return doubled_positives
```

### Pattern 15: Consistent Naming Conventions
**Problem**: Inconsistent naming styles
**Solution**: Apply consistent conventions

**Before**:
```python
class userManager:
    def GetUserName(self):
        pass
    
    def update_user_email(self):
        pass
    
    def DeleteUserAccount(self):
        pass
```

**After**:
```python
class UserManager:
    def get_user_name(self):
        pass
    
    def update_user_email(self):
        pass
    
    def delete_user_account(self):
        pass
```

## Type Safety Patterns

### Pattern 16: Type Annotation Improvement
**Problem**: Missing or incorrect type annotations
**Solution**: Add proper type hints

**Before**:
```python
def process_data(data):
    result = {}
    for key, value in data.items():
        result[key] = str(value)
    return result
```

**After**:
```python
from typing import Dict, Any

def process_data(data: Dict[str, Any]) -> Dict[str, str]:
    result: Dict[str, str] = {}
    for key, value in data.items():
        result[key] = str(value)
    return result
```

### Pattern 17: Optional Type Handling
**Problem**: Unclear optional values
**Solution**: Use Optional type

**Before**:
```python
def find_user(user_id):
    # Returns user or None
    pass

user = find_user(123)
if user:
    print(user.name)
```

**After**:
```python
from typing import Optional

def find_user(user_id: int) -> Optional[User]:
    # Returns user or None
    pass

user = find_user(123)
if user:
    print(user.name)
```

## Async/Await Patterns

### Pattern 18: Callback to Async/Await
**Problem**: Callback hell
**Solution**: Convert to async/await

**Before**:
```javascript
function fetchData(callback) {
    getConfig(function(config) {
        getUser(config.userId, function(user) {
            getData(user.id, function(data) {
                callback(null, data);
            }, function(error) {
                callback(error);
            });
        }, function(error) {
            callback(error);
        });
    }, function(error) {
        callback(error);
    });
}
```

**After**:
```javascript
async function fetchData() {
    try {
        const config = await getConfig();
        const user = await getUser(config.userId);
        const data = await getData(user.id);
        return data;
    } catch (error) {
        throw error;
    }
}
```

### Pattern 19: Parallel Execution
**Problem**: Sequential async operations
**Solution**: Execute in parallel

**Before**:
```javascript
async function fetchAllData() {
    const users = await fetchUsers();
    const products = await fetchProducts();
    const orders = await fetchOrders();
    return { users, products, orders };
}
```

**After**:
```javascript
async function fetchAllData() {
    const [users, products, orders] = await Promise.all([
        fetchUsers(),
        fetchProducts(),
        fetchOrders()
    ]);
    return { users, products, orders };
}
```

## Class and Object Patterns

### Pattern 20: Replace Primitive with Object
**Problem**: Primitive values with behavior
**Solution**: Create value objects

**Before**:
```python
def calculate_total(price, quantity, tax_rate):
    subtotal = price * quantity
    tax = subtotal * tax_rate
    return subtotal + tax
```

**After**:
```python
class Money:
    def __init__(self, amount, currency='USD'):
        self.amount = amount
        self.currency = currency
    
    def __mul__(self, multiplier):
        return Money(self.amount * multiplier, self.currency)
    
    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError("Currency mismatch")
        return Money(self.amount + other.amount, self.currency)

def calculate_total(price, quantity, tax_rate):
    subtotal = price * quantity
    tax = subtotal * tax_rate
    return subtotal + tax

# Usage
price = Money(10.99)
total = calculate_total(price, 3, 0.08)
```

### Pattern 21: Replace Conditional with Polymorphism
**Problem**: Type-based conditionals
**Solution**: Use polymorphism

**Before**:
```python
class Animal:
    def make_sound(self, animal_type):
        if animal_type == 'dog':
            return 'Woof!'
        elif animal_type == 'cat':
            return 'Meow!'
        elif animal_type == 'bird':
            return 'Chirp!'
        else:
            return 'Unknown animal'
```

**After**:
```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def make_sound(self):
        pass

class Dog(Animal):
    def make_sound(self):
        return 'Woof!'

class Cat(Animal):
    def make_sound(self):
        return 'Meow!'

class Bird(Animal):
    def make_sound(self):
        return 'Chirp!'
```

## Functional Patterns

### Pattern 22: Function Composition
**Problem**: Nested function calls
**Solution**: Compose functions

**Before**:
```python
def process_data(data):
    cleaned = clean_data(data)
    transformed = transform_data(cleaned)
    validated = validate_data(transformed)
    return validated
```

**After**:
```python
from functools import reduce

def compose(*functions):
    def composed(arg):
        return reduce(lambda result, f: f(result), functions, arg)
    return composed

process_data = compose(clean_data, transform_data, validate_data)
```

### Pattern 23: Higher-Order Functions
**Problem**: Repeated patterns with slight variations
**Solution**: Use higher-order functions

**Before**:
```python
def filter_even(numbers):
    result = []
    for n in numbers:
        if n % 2 == 0:
            result.append(n)
    return result

def filter_positive(numbers):
    result = []
    for n in numbers:
        if n > 0:
            result.append(n)
    return result

def filter_prime(numbers):
    result = []
    for n in numbers:
        if is_prime(n):
            result.append(n)
    return result
```

**After**:
```python
def filter_numbers(numbers, predicate):
    return [n for n in numbers if predicate(n)]

filter_even = lambda nums: filter_numbers(nums, lambda n: n % 2 == 0)
filter_positive = lambda nums: filter_numbers(nums, lambda n: n > 0)
filter_prime = lambda nums: filter_numbers(nums, is_prime)
```

## Pattern Selection Guidelines

### When to Use Each Pattern

| Pattern | Best For | Complexity Reduction | Risk Level |
|---------|----------|---------------------|------------|
| Early Return | Deeply nested conditionals | High | Low |
| Guard Clauses | Validation-heavy code | Medium | Low |
| Decomposition | Long functions (>50 lines) | High | Medium |
| Boolean Simplification | Complex boolean logic | Medium | Low |
| Switch/Case | Long if-else chains | High | Low |
| Null Object | Frequent null checks | Medium | Low |
| Extract Method | Reusable code blocks | Medium | Low |
| Extract Class | Related function groups | High | Medium |
| Type Annotations | Dynamic language code | High | Low |
| Async/Await | Callback-based async code | High | Medium |

### Pattern Combination Strategies

**Strategy 1: Bottom-Up Refactoring**
1. Start with Extract Method for small blocks
2. Apply Early Return for conditionals
3. Use Decomposition for large functions
4. Finish with Extract Class if needed

**Strategy 2: Top-Down Refactoring**
1. Start with Extract Class to define boundaries
2. Apply Decomposition within classes
3. Use Extract Method for details
4. Finish with Early Return and Guard Clauses

**Strategy 3: Language-Specific Approach**
- **Python**: Focus on comprehensions, decorators, type hints
- **JavaScript**: Focus on async/await, functional patterns
- **TypeScript**: Focus on type safety, interfaces
- **Java**: Focus on design patterns, streams

### Anti-Patterns to Avoid

1. **Over-Engineering**: Don't apply patterns where they're not needed
2. **Premature Optimization**: Focus on readability first, performance second
3. **Pattern Misuse**: Don't force patterns that don't fit the problem
4. **Incomplete Refactoring**: Finish what you start, or revert
5. **Ignoring Tests**: Always verify functionality after refactoring

These patterns provide a comprehensive toolkit for code simplification across different languages and scenarios. The code-simplifier skill intelligently applies these patterns based on code analysis and configuration settings.