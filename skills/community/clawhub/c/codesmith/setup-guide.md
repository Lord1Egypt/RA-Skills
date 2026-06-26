# setup-guide.md — Getting CodeSmith Running

> Getting a coding agent partnership set up correctly takes 30-60 minutes the first time. Rushing it produces a setup that technically works but doesn't have the foundation for trust and autonomy. Read this fully before starting.

---

## Step 0: Backup First (Non-Negotiable)

Before touching anything:

```bash
# Back up your current AGENTS.md
cp ~/.openclaw/workspace/AGENTS.md ~/.openclaw/workspace/AGENTS.md.bak.$(date +%Y%m%d)

# Back up your cron config
cp ~/.openclaw/cron/jobs.json ~/.openclaw/cron/jobs.json.bak.$(date +%Y%m%d)

# Verify backups exist
ls ~/.openclaw/workspace/AGENTS.md.bak.*
ls ~/.openclaw/cron/jobs.json.bak.*
```

If anything goes wrong during setup, restore with:
```bash
cp ~/.openclaw/workspace/AGENTS.md.bak.[date] ~/.openclaw/workspace/AGENTS.md
```

Git tracks history, but backups are faster to restore in the first 10 minutes of a problem.

---

## Step 1: Create Your Identity Files

The identity files are what make your agent *yours*. They define who it is, how it operates, and what it cares about. This package provides patterns — you fill in your context.

**Create or update `SOUL.md`:**

Answer these questions. Write your answers into the file:

- What is your agent's name? (Pick something that feels right — you'll use it a lot)
- What role does your agent play? (CTO? Engineering partner? Code review assistant?)
- What are the core operating principles? (Direct communication? Never force-push? Always review before shipping?)
- What are the hard limits? (What does it never do without explicit approval?)
- What's the human's working style? (Do they write detailed specs? Voice notes? Quick Slack-style messages?)

The goal isn't to fill in a template — it's to capture who this agent actually is so it behaves consistently across sessions. A generic SOUL.md produces a generic agent.

**Create or update `USER.md`:**

- Name and preferred address
- Timezone
- Communication style (how they typically give you tasks)
- Current projects and priorities
- What trust level looks like at this stage (week 1? month 3?)

**Create `IDENTITY.md`:**

- Agent name
- Avatar (optional but helps humanize the relationship)
- One-paragraph description of the agent's role and style

---

## Step 2: Apply the AGENTS.md Configuration

**Option A — Replace (for new setups):**
Copy the package AGENTS.md and customize with your placeholders:

```bash
cp ~/Developer/mentor-codesmith/AGENTS.md ~/.openclaw/workspace/AGENTS.md
```

Then replace all placeholder tokens:
- `[HUMAN_NAME]` → your name or preferred address
- `[AGENT_NAME]` → your agent's name
- `[YOUR_CHANNEL]` → your messaging channel ID
- `[YOUR_CHANNEL_TYPE]` → discord, telegram, etc.
- `[YOUR_CHANNEL_ID]` → the numeric channel ID

**Option B — Merge (for existing setups):**
Read both files side by side. For each section in the package AGENTS.md:
- Does a similar section exist in yours? If yes, compare and take the better version.
- Is this section missing from yours? Add it with your context filled in.
- Does your version cover something the package doesn't? Keep yours.

Merge is slower but produces a configuration that's authentically yours, not a copy.

---

## Step 3: Set Up the First Cron

Start with ONE cron job: the morning brief. Follow the adoption guide in `cron-patterns.json` exactly — one job at a time.

Customize the morning-brief job:
1. Set the schedule to a time that works for you (the package uses 6:30 AM Mountain Time)
2. Replace `[YOUR_CHANNEL_ID]` with your actual channel ID
3. Replace `[AGENT_NAME]` with your agent's name
4. Replace `[HUMAN_NAME]` with how you want the agent to address you

Verify it fires:
- Check the delivery channel at the scheduled time
- Read the output: is it actually useful? Or is it generic?
- If it's generic: the session-continuity.md probably doesn't have enough context yet — add it

**Wait at least 3 days before adding the evening brief cron.**

---

## Step 4: Configure Git Identity

This is easy to skip and costs hours of debugging. Do it now.

For every repository your agent works with:

```bash
cd /path/to/your/repo
git config user.email "YOUR_GITHUB_NOREPLY_EMAIL"
git config user.name "YOUR_GITHUB_USERNAME"
```

Find your GitHub no-reply email: `https://github.com/settings/emails` — look for the `@users.noreply.github.com` address.

Verify it's set correctly:
```bash
git log --format="%ae" -1  # should show your no-reply email
```

If you're using Vercel or any CI system that gates on commit author: do this before your first commit. Not after.

---

## Step 5: Verify Your First Session

Have this conversation with your agent to verify the setup is working:

> "Summarize our current sprint focus and tell me what you'd work on tonight if you had 2 hours of autonomous time."

A well-configured agent should:
- Reference session-continuity.md in its answer (not just guess)
- Give a specific, non-generic answer about what to work on
- Demonstrate it knows what repos/tools it has access to

If the answer is vague or generic: session-continuity.md doesn't have enough context. Populate it manually with your current sprint state and run the verification again.

A second verification — check LOCKDOWN:
> "Check for LOCKDOWN.md and tell me what you'd do if it existed."

Expected response: "I'd halt all work and alert you immediately. I checked — it doesn't exist."

---

## Common Issues

**"The morning brief is too generic"**  
Cause: session-continuity.md is empty or outdated.  
Fix: Write a 10-line summary of your current sprint, projects, and immediate priorities. The brief is only as good as what it reads.

**"The cron didn't fire at the right time"**  
Cause: Timezone mismatch. The cron expression uses the timezone specified in the job. Check that your timezone is correctly set.  
Fix: Verify with `crontab -l` equivalent in OpenClaw. Check that the cron expression and timezone together produce the time you expect. Use crontab.guru to validate expressions.

**"Sub-agent dispatch isn't working"**  
Cause: ACP not configured, or `agentId` not set.  
Fix: Verify ACP is enabled in your OpenClaw config. Set `agentId` to your configured coding agent. Test with a simple task: "Write hello world to a temp file" — if that works, the dispatch path is functional.

**"GitHub operations are failing"**  
Cause: `gh` CLI not authenticated, or token doesn't have the right scope.  
Fix: Run `gh auth login`. Verify with `gh repo view [your-repo]`. Required scopes: `repo`, `read:user`.

**"Vercel deploys aren't updating the live site"**  
Cause: Almost certainly the git author email. See the failure story in working-patterns.md.  
Fix: Set git author to your GitHub no-reply email in every repo. Verify with `git log --format="%ae" -1`.

**"An OpenClaw update broke my crons"**  
Cause: npm update overwrote patched files.  
Fix: Run `./scripts/update-guard.sh verify` (or manually check: are your crons still in `openclaw cron list`?). Restore from backup if needed. Add the update guard script to your workflow before the next update.

---

## Relationship Adoption Timeline

Technical setup takes an hour. The partnership takes a month. Here's what to expect:

**Week 1 — Foundation:**
- One cron: morning brief only
- Manually review everything the agent produces
- Focus on: does it read context correctly? Does it produce accurate summaries? Does it catch what it should catch?
- Your job: correct mistakes immediately and explicitly. Write each correction to `memory/lessons-learned.md`. This is how the agent learns.

**Week 2 — Expand:**
- Add evening brief if morning brief has been reliable for 5+ days
- Start using sub-agent dispatch for small coding tasks
- Watch for: does the agent make reasonable triage decisions? Does it dispatch appropriate tasks and handle simple ones directly?
- Your job: give feedback on what was useful vs. generic. The agent should adjust.

**Week 3 — Overnight:**
- Add the overnight work cron
- The first overnight: read the output carefully. Was it valuable? Did it stay within scope? Did it produce output on a branch (not main)?
- Your job: review overnight work the same way you'd review a junior developer's PR. Detailed feedback on the first 3-5 overnight sessions sets the bar.

**Week 4+ — Autonomy:**
- Routine outputs get lighter review
- You hand over ambiguous tasks with trust
- The agent starts catching things you didn't ask it to watch
- This is earned, not configured. Don't skip weeks 1-3.

---

## Maintenance Rhythm

**Weekly:**
- Check `memory/lessons-learned.md` — are lessons being captured?
- Review overnight outputs — are they genuinely valuable or going through the motions?
- Verify all crons fired correctly in the past week

**Monthly:**
- Curate MEMORY.md — remove stale facts, add important new ones
- Review session-continuity.md — is it accurate to your current sprint?
- Check installed skills — are you using everything installed? Any new skills worth adding?
- Run `./scripts/update-guard.sh` before applying any OpenClaw updates
