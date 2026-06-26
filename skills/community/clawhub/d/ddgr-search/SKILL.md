# DDGR Search Skill

This skill provides a web search capability using `ddgr`.

## Description
Use `ddgr` to perform web searches from the command line. This skill wraps the `ddgr` command for easy use.

## Tools
```yaml
tools:
  - id: ddgr_search
    description: Perform a web search using ddgr.
    type: exec
    command: ["ddgr", "-n", "{{args.count}}", "{{args.query}}"]
    args:
      query:
        type: string
        description: The search query.
      count:
        type: integer
        description: The number of results to return (default 5).
        default: 5
```

## Usage Example
```
/ddgr_search "openclaw telegram bot exec tool"
```
