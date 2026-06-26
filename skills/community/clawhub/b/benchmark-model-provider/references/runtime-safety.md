# Runtime Safety

## Trust boundary

This skill can send prompts and model outputs to external endpoints depending on the benchmark spec and delivery choice.

## Network behavior

### Benchmark execution
- `run_benchmark.py` sends prompts to the `base_url` configured in the benchmark spec
- only use trusted endpoints
- if the endpoint is remote, prompts and API credentials may leave the local machine

### Publishing
- `publish_report.py` can publish benchmark HTML to Vercel when the user explicitly chooses web delivery
- do not publish sensitive prompts, outputs, or internal reports without review

## Safe defaults
- examples use placeholder URLs such as `https://api.example.com/v1`
- real credentials should come from environment variables, not example files
- users should review specs before executing benchmark or publish steps

## Recommended safe usage
- test first with non-sensitive prompts
- use isolated environments when evaluating new endpoints or dependencies
- verify the benchmark spec before running or publishing
