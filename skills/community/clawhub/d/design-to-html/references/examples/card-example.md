# Example 2: Card Component

## Design Input

A product card design with:
- Size: 400x300px
- Background: white (#FFFFFF)
- Image area: top 50%, placeholder image
- Title: "Product Name", 24px, bold, black
- Price: "$99.00", 20px, gray (#666666)
- Button: "Add to Cart", 16px, blue (#0066CC)
- Padding: 20px
- Border-radius: 12px
- Shadow: 0 4px 12px rgba(0,0,0,0.1)

## Initial HTML (Iteration 1)

```html
<!DOCTYPE html>
<html>
<head>
<style>
body {
    width: 400px;
    height: 300px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #F5F5F5;
}
.card {
    width: 400px;
    height: 300px;
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    padding: 20px;
}
.image-placeholder {
    width: 100%;
    height: 150px;
    background: #DDD;
}
.title {
    font-size: 24px;
    font-weight: bold;
    color: black;
}
.price {
    font-size: 20px;
    color: #666666;
}
button {
    padding: 10px 20px;
    background: #0066CC;
    color: white;
    border: none;
    border-radius: 4px;
}
</style>
</head>
<body>
<div class="card">
    <div class="image-placeholder"></div>
    <h2 class="title">Product Name</h2>
    <p class="price">$99.00</p>
    <button>Add to Cart</button>
</div>
</body>
</html>
```

**Match score**: 78.5%

## Diff Report (Iteration 1)

```json
{
    "matchScore": 78.5,
    "diffPixels": 21600,
    "totalPixels": 120000,
    "issues": [
        {
            "type": "spacing",
            "description": "Title and price spacing incorrect",
            "severity": "high"
        },
        {
            "type": "layout",
            "description": "Button position mismatch",
            "severity": "medium"
        },
        {
            "type": "color",
            "description": "Shadow opacity slightly off",
            "severity": "low"
        }
    ]
}
```

## Optimized HTML (Iteration 5)

After 5 iterations of optimization based on diff reports:

```html
<!DOCTYPE html>
<html>
<head>
<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}
body {
    width: 400px;
    height: 300px;
    background: #F5F5F5;
}
.card {
    width: 400px;
    height: 300px;
    background: #FFFFFF;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    padding: 20px;
    display: flex;
    flex-direction: column;
}
.image-placeholder {
    width: 360px;
    height: 150px;
    background: #DDD;
    border-radius: 8px;
    margin-bottom: 16px;
}
.content {
    display: flex;
    flex-direction: column;
    gap: 8px;
}
.title {
    font-size: 24px;
    font-weight: bold;
    color: #000000;
}
.price {
    font-size: 20px;
    color: #666666;
    margin-top: 4px;
}
.button-container {
    margin-top: 12px;
}
button {
    padding: 10px 20px;
    background: #0066CC;
    color: #FFFFFF;
    border: none;
    border-radius: 4px;
    font-size: 16px;
    cursor: pointer;
}
</style>
</head>
<body>
<div class="card">
    <div class="image-placeholder"></div>
    <div class="content">
        <h2 class="title">Product Name</h2>
        <p class="price">$99.00</p>
        <div class="button-container">
            <button>Add to Cart</button>
        </div>
    </div>
</div>
</body>
</html>
```

**Match score**: 91.8%

## Result

⚠️ **Below threshold** (91.8% < 95%)

**Final HTML**: Iteration 5 (best result)
**Iterations**: 5/5 (max reached)
**Recommendation**: Manual tweaks needed for exact match
- Fine-tune shadow opacity
- Adjust button positioning pixel-by-pixel