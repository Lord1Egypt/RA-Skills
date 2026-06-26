# Troubleshooting

## Safe Recovery Order

Use this order to reduce damage:
1. verify the target profile and install path
2. reproduce the issue once without changing anything
3. compare with a private or disposable session
4. disable the smallest suspect extension set
5. test per-site Shields changes
6. compare with a fresh profile
7. only then consider cache, cookie, or profile cleanup

## Startup Failures

If Brave will not launch or crashes immediately:
- check whether the wrong channel or binary path is being used
- remove risky flags from the last launch attempt
- test with a clean profile before touching the main one
- record the exact symptom: no window, flash then close, or freeze

## Update and State Problems

When Brave changed behavior after an update:
- separate browser-version change from extension change
- confirm whether the problem is global or profile-specific
- avoid mass cleanup before one controlled comparison run

## When to Stop

Stop and get explicit approval before:
- deleting profile data
- clearing cookies for important accounts
- changing global privacy posture
- leaving remote debugging enabled
- touching sync or wallet configuration
