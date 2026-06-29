# Precision Runtime Compatibility

A runtime is precision-compatible only when it documents all of these explicitly:

- which precision files it reads
- which advisory fields it emits
- which precision checks it can execute
- whether any advisory result can influence control flow through repo-local runtime policy
- how unsupported precision features degrade

## Minimum Precision Compatibility

A minimally precision-compatible runtime supports:

- reading `profile.json`
- reading `tuning.json`
- treating profile commands as defaults only
- treating footer verification fields as round truth
- writing precision state separately from core state
- ignoring unknown precision fields safely
- enforcing `precisionAdvice` as `none|warn|pause_review` only
- enforcing `roundScore` as `null` or integer `0-100`
- enforcing `hooksExecuted` items as objects with `name` and `status`

## Not Required

A runtime does not need scoring to be precision-compatible. It may implement profiles and tuning first.
