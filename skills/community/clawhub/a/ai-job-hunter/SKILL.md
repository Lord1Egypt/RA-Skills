# AI Job Hunter

Automatically scan remote job boards and find opportunities matching your skills.

## Features
- Scans Remote OK, We Work Remotely, Hacker News Jobs
- Filters by keywords (AI, Python, TypeScript, Remote)
- Generates personalized cover letters
- Daily digest of new opportunities

## Usage
```
/job-hunt [keywords] [--salary min] [--remote-only]
```

## Examples
```
/job-hunt "AI engineer" --salary 100000 --remote-only
/job-hunt "TypeScript developer"
```

## Output
- Job title, company, salary range
- Match score based on your profile
- Auto-generated cover letter draft

## Configuration
Set your profile in `~/.openclaw/workspace/USER.md` for better matching.
