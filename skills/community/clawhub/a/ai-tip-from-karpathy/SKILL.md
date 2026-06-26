# AI Tip from @karpathy

## Description
Automatically generated AI learning skill from curated web and social media sources.

## Steps

1. Tip: When training neural nets, always start with a tiny dataset (e.g. 10 examples) and overfit it completely before scaling up. This validates your entire pipeline works end-to-end.
2. # Test your training loop
3. def test_overfit():
4. model = YourModel()
5. tiny_dataset = get_tiny_dataset(10)
6. train(model, tiny_dataset, epochs=1000)
7. assert loss < 0.01

## Code Examples

```python
# Test your training loop
def test_overfit():
    model = YourModel()
    tiny_dataset = get_tiny_dataset(10)
    train(model, tiny_dataset, epochs=1000)
    assert loss < 0.01
```
