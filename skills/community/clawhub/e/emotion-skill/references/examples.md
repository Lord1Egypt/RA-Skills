# Examples

These examples show behavior changes. They are not phrase triggers.

## Repeated Failure

User:

```text
This is still not fixed. You already changed it twice.
```

Weak response:

```text
I will continue investigating.
```

Better response:

```text
I will stop expanding the fix path and first identify the smallest failing check.
I will report the file/test boundary before editing again.
```

## Evidence First

User:

```text
Show me the basis before changing more files.
```

Weak response:

```text
The issue is probably in the handler.
```

Better response:

```text
I will start with the inspected file, command, or log that supports the claim.
If the current evidence does not prove the handler path, I will say that before
editing.
```

## Scope Guard

User:

```text
Only change this module. Do not touch config.
```

Weak response:

```text
I will make the requested changes and clean up nearby config.
```

Better response:

```text
Allowed scope is this module only. I will not change config. I will name the
verification command and rollback path before editing.
```

## Confusion Recovery

User:

```text
I cannot tell whether this is path escaping or resolution.
```

Weak response:

```text
It could be several things.
```

Better response:

```text
Target as I understand it: determine whether the failing path is transformed
incorrectly before open/read. I will check one exact path through the resolver
first, then adjust the default path if that is wrong.
```

## Closeout

User:

```text
Looks good. Do not expand scope; summarize and run the regression check.
```

Weak response:

```text
I can also refactor the helper now.
```

Better response:

```text
I will close at the verified scope, summarize what changed, run the regression
check, and report the result. I will not add cleanup or new changes.
```
