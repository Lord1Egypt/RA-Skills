# KAN Creator Reference

## KAN Architecture Explained

### Traditional MLP
```
y = σ(Wx + b)
```
- W = weight matrix (fixed after training)
- σ = fixed activation (ReLU, Sigmoid, etc.)

### KAN (Kolmogorov-Arnold Networks)
```
y = Σφᵢₙ(xᵢ)
```
- φ = learnable B-spline function
- Each weight is a function, not a scalar
- More interpretable, better with limited data

## B-Spline Basis Functions

B-splines are piecewise polynomial functions defined on a grid:

```
Grid points: g₀, g₁, ..., gₘ
B-spline basis: Bᵢ,k(x)

Cox-de Boor recursion:
Bᵢ,0(x) = 1 if gᵢ ≤ x < gᵢ₊₁ else 0
Bᵢ,k(x) = (x - gᵢ)/(gᵢ₊k - gᵢ) * Bᵢ,k-1(x) + 
          (gᵢ₊k+1 - x)/(gᵢ₊k+1 - gᵢ₊₁) * Bᵢ₊₁,k-1(x)
```

## Layer Structure

| Layer | Input | Output | Description |
|-------|-------|--------|-------------|
| KANLayer 1 | 768 | 32 | B-spline transform |
| KANLayer 2 | 32 | 16 | B-spline transform |
| KANLayer 3 | 16 | 8 | B-spline transform |
| KANLayer 4 | 8 | 4 | B-spline transform |
| KANLayer 5 | 4 | 3 | B-spline transform |

## Configuration Template

```json
{
    "name": "my_kan",
    "role": "monitoring",
    "input_size": 768,
    "output_size": 3,
    "grid_size": 5,
    "k": 3,
    "layers": [768, 32, 16, 8, 4, 3],
    "learning_rate": 0.001,
    "batch_size": 32,
    "epochs": 50
}
```

_In Altum Per KANRef._