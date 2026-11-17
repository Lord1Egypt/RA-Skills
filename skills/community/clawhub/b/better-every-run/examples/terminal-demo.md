# Terminal Demo

Record the Better Every Run terminal demo with asciinema:

```bash
asciinema rec --overwrite -q -i 1.0 -t "Better Every Run v0.5.5" \
  -c "bash examples/asciinema-demo.sh" \
  assets/better-every-run-terminal-demo.cast
```

Render the inline README artifact:

```bash
npx --yes svg-term-cli@2.1.1 --in assets/better-every-run-terminal-demo.cast \
  --out assets/better-every-run-terminal-demo.svg --window --width 100 --height 32
```

Play the committed recording locally:

```bash
asciinema play assets/better-every-run-terminal-demo.cast
```

The script runs in a temporary directory and leaves no `.better-every-run/` state in the repo.
