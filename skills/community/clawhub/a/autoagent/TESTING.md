# Testing the Autoagent Skill

## Manual Test

1. Create test sandbox:
```bash
mkdir -p /tmp/autoagent-test
cd /tmp/autoagent-test
```

2. Copy example:
```bash
cp /home/peterwsl/clawd/skills/autoagent/examples/simple-news-prompt.md ./test-guidance.md
```

3. Create fixtures manually to verify format

4. Run through iteration logic mentally

## Integration Test (OpenClaw)

Once OpenClaw is set up:
1. Invoke /autoagent
2. Answer questions with test paths
3. Verify sandbox creation
4. Verify cron setup
5. Check scores.md after iterations
