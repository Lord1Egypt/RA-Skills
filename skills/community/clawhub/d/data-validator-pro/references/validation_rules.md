# Validation Rules Reference

## Type Checks

- `int` - Integer dtype
- `float` - Float dtype
- `str` - String dtype
- `bool` - Boolean dtype
- `datetime` - Datetime64 dtype

## Constraints

- `min` / `max` - Numeric range (inclusive)
- `regex` - String pattern match
- `unique` - No duplicate values
- `enum` - Value must be in allowed list
- `nullable` - Whether nulls are allowed (default True)

## Example Schema

```python
schema = {
    "user_id": {"type": "int", "unique": True, "nullable": False},
    "age": {"type": "int", "min": 0, "max": 150},
    "email": {"type": "str", "regex": r"^\S+@\S+\.\S+$"},
    "country": {"type": "str", "enum": ["US", "UK", "CN", "JP"]},
    "score": {"type": "float", "min": 0.0, "max": 100.0},
}
```

## Anomaly Detection Methods

- **IQR** - Interquartile range (1.5 * IQR rule)
- **Z-Score** - Standard deviations from mean
- **MAD** - Median absolute deviation (robust to outliers)
