# Example 1: Button Component

## Design Input

A simple button design with:
- Size: 200x50px
- Background: #FF5733 (orange)
- Text: "Click Me", white, 16px, bold
- Border-radius: 8px
- Centered text

## Initial HTML (Iteration 1)

```html
<!DOCTYPE html>
<html>
<head>
<style>
body {
    width: 200px;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
}
button {
    width: 200px;
    height: 50px;
    background: #FF5733;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    font-weight: bold;
}
</style>
</head>
<body>
<button>Click Me</button>
</body>
</html>
```

**Match score**: 92.3%

## Diff Report (Iteration 1)

```json
{
    "matchScore": 92.3,
    "diffPixels": 770,
    "totalPixels": 10000,
    "issues": [
        {
            "type": "spacing",
            "description": "Button text slightly off-center (2px horizontal offset)",
            "severity": "low"
        }
    ]
}
```

## Optimized HTML (Iteration 2)

```html
<!DOCTYPE html>
<html>
<head>
<style>
body {
    width: 200px;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0;
    padding: 0;
}
button {
    width: 200px;
    height: 50px;
    background: #FF5733;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    font-weight: bold;
    padding: 0;
    margin: 0;
    display: flex;
    align-items: center;
    justify-content: center;
}
</style>
</head>
<body>
<button>Click Me</button>
</body>
</html>
```

**Match score**: 96.1%

## Result

✅ **Threshold reached** (96.1% > 95%)

**Final HTML**: Same as Iteration 2
**Iterations**: 2/5
**Time**: ~15 seconds