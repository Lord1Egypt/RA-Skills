# Diff acquisition

## Default mode

Assume the current working repository is the review target unless the user specifies otherwise.

Recommended sequence:
1. inspect status
2. inspect unstaged diff
3. inspect staged diff
4. if needed, inspect recent commits or a requested revision range

## Supported input forms

### Working tree review
Use the repository's current changes.

### Revision range review
Use `git diff <base>..<head>` when the user names two revisions.

### Single-commit review
Use `git show <commit>` or compare the commit to its parent when the user asks for one commit.

### Pull request diff
If the pr diff is available directly, review that artifact. If not, reconstruct from available refs only when the environment clearly supports it.

### Raw patch review
If the user pasted a patch or diff, review the provided text and inspect repository context only when needed.

## Fallback behavior

If the first diff attempt is empty or confusing:
- verify repository state
- distinguish staged vs unstaged work
- verify working directory and branch context
- check whether the user intended a revision range instead

## Large diff behavior

When the diff is too large to review exhaustively:
- prioritize risky files and interfaces first
- state the narrowed scope clearly
- still note any obvious repository-wide patterns, especially repeated bloat or missing tests
