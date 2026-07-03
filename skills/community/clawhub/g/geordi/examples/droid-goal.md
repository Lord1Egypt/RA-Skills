# Example Droid goal

Goal: Fix validation on a checkout form using a configured Droid custom model.

```bash
geordi init --goal "Fix checkout validation" --mode droid
geordi mission add "Repair invalid email and empty address validation" --accept "npm test -- checkout" --scope "Checkout form, validation helper, and tests only."
geordi run --mode droid --model "custom:Your-Model-0"
```

If your shared agent rules live outside the default `~/.agents/AGENTS.md` path:

```bash
GEORDI_AGENTS_FILE=/path/to/AGENTS.md geordi run --mode droid --model "custom:Your-Model-0"
```
