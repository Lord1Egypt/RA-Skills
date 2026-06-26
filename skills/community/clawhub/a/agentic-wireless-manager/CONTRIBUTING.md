# Contributing to Agentic Liquid Wireless Manager

Thank you for your interest in contributing.

## How to Contribute

1. **Fork** the repository
2. **Create a branch** for your feature or fix
3. **Make your changes** with clear commit messages
4. **Test** on at least one platform (macOS, Linux, or Windows)
5. **Submit a pull request** with a description of what you changed and why

## Areas Where Help Is Needed

- **Cross-platform testing:** Verify commands work on different Linux distros, Windows versions, macOS versions
- **Training improvements:** More episodes, curriculum learning, hyperparameter tuning
- **New interference signatures:** Add detection patterns for more device types (Zigbee, Z-Wave, etc.)
- **Spatial calibration:** Better algorithms for directional accuracy with limited APs
- **Integration guides:** Step-by-step guides for more agentic AI platforms
- **Documentation:** Translations, tutorials, video walkthroughs

## Code Style

- Python 3.8+ compatible
- No external dependencies beyond PyTorch and NumPy for the core agent
- OS commands must work without elevated privileges for read operations
- All admin/sudo commands must be documented in `docs/PERMISSIONS_AND_CONTROLS.md`
- Plain English output — avoid jargon in user-facing messages

## Testing

```bash
# Run self-test
python3 sac_ltc_agent.py --test

# Train and evaluate
python3 train_sac_ltc.py --episodes 1000
python3 train_sac_ltc.py --eval
```

## Disclosure Policy

This project is fully transparent:
- Every neural architecture component is documented
- Every OS command is listed with exact syntax
- Every permission is disclosed
- Training data generation is reproducible
- No obfuscated code, no hidden capabilities

Contributions must maintain this transparency standard.
