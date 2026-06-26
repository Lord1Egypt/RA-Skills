# Procedures — Operational Standards Checklist

This document outlines 14 standard operational procedures for managing an AI agent workspace. Each procedure is a checklist that can be performed by designated agents, administrators, or team members as needed.

## Procedure 1: Agent Workspace Onboarding

**Frequency:** Once per new agent
**Owner:** Administrator
**Duration:** 30-60 minutes
**Dependencies:** GOVERNANCE.md, agent config file

**Checklist:**

- [ ] Create agent workspace directory structure
- [ ] Create IDENTITY.md (agent role, capabilities, responsibilities)
- [ ] Create CONTEXT.md (organizational priorities, stakeholders, constraints)
- [ ] Create BOOTSTRAP.md with initialization instructions
- [ ] Create `memory/` directory for daily logs
- [ ] Initialize empty `MEMORY.md`
- [ ] Copy GOVERNANCE.md, PROCEDURES.md, DELEGATION.md to workspace
- [ ] Create TOOLS.md (empty file for agent to populate)
- [ ] Create or link agent config file (agent-config.json or equivalent)
- [ ] Document workspace path and access credentials
- [ ] Schedule first check-in with agent
- [ ] Verify agent can read all required files
- [ ] Run agent on first session and confirm initialization
- [ ] Collect feedback on documentation clarity
- [ ] Archive initialization checklist in workspace history

## Procedure 2: Configuration Management

**Frequency:** On demand (when settings change)
**Owner:** Administrator or designated agent
**Duration:** 15-30 minutes
**Dependencies:** agent-config.json or equivalent

**Checklist:**

- [ ] Document current configuration (create backup)
- [ ] Identify what's changing and why
- [ ] Update agent-config.json with new settings
- [ ] Validate syntax and structure of config file
- [ ] Identify agents affected by this change
- [ ] Notify affected agents of configuration change
- [ ] Schedule config reload in next session
- [ ] Log configuration change with timestamp and reason
- [ ] Test critical functionality post-update
- [ ] Create rollback plan if issues occur
- [ ] Document new configuration in PROCEDURES.md
- [ ] Update any related documentation

## Procedure 3: Memory Audit and Cleanup

**Frequency:** Weekly or bi-weekly
**Owner:** Agent (with oversight)
**Duration:** 20-40 minutes
**Dependencies:** memory/ directory, MEMORY.md

**Checklist:**

- [ ] List all daily memory files (memory/YYYY-MM-DD.md)
- [ ] Identify files older than 30 days
- [ ] Review recent files (last 7 days) for significant events
- [ ] Extract lessons and insights worth keeping
- [ ] Update MEMORY.md with new long-term insights
- [ ] Remove outdated entries from MEMORY.md
- [ ] Archive older daily files to an archive directory (don't delete)
- [ ] Verify MEMORY.md is secure and not shared
- [ ] Check memory file sizes (warn if any file >100KB)
- [ ] Document memory maintenance actions taken
- [ ] Communicate significant findings to administrator if needed

## Procedure 4: Daily Standup

**Frequency:** Once daily (or multiple times for multi-shift teams)
**Owner:** Administrator
**Duration:** 15-30 minutes
**Dependencies:** Agent memory files, open tasks

**Checklist:**

- [ ] Request or retrieve agent's daily summary
- [ ] Review recent memory entries (last 24 hours)
- [ ] Identify completed tasks and outcomes
- [ ] Identify in-progress work and blockers
- [ ] Identify planned work for remainder of day
- [ ] Check agent health (any error logs or issues?)
- [ ] Discuss any escalations or decisions needed
- [ ] Document standup notes in shared location
- [ ] Confirm agent has resources needed to proceed
- [ ] Schedule next check-in

## Procedure 5: Task Escalation Protocol

**Frequency:** As needed when agent hits limitation
**Owner:** Agent or Administrator
**Duration:** 10-20 minutes
**Dependencies:** GOVERNANCE.md, communication channel

**Checklist:**

- [ ] Agent identifies task or decision beyond their authority
- [ ] Agent documents reason escalation is needed
- [ ] Agent notifies administrator with clear context
- [ ] Include: task description, blocker, recommended action
- [ ] Provide relevant memory files or documentation
- [ ] Administrator reviews escalation within SLA (e.g., 2 hours)
- [ ] Administrator makes decision or delegates further
- [ ] Administrator communicates decision back to agent
- [ ] Agent updates memory with decision and rationale
- [ ] Continue task with new authority/context
- [ ] Close escalation ticket and document outcome

## Procedure 6: Cross-Agent Delegation

**Frequency:** Multiple times per week (as needed)
**Owner:** Delegating agent or administrator
**Duration:** 20-45 minutes
**Dependencies:** DELEGATION.md, target agent workspace

**Checklist:**

- [ ] Follow Delegation Lifecycle in DELEGATION.md (request → execute → verify → close)
- [ ] Create delegation request with clear specs
- [ ] Identify delegated agent and verify availability
- [ ] Document delegation in DELEGATION.md audit trail
- [ ] Target agent confirms receipt and understanding
- [ ] Target agent estimates completion time
- [ ] Confirm any context the target agent needs
- [ ] Set verification criteria before work starts
- [ ] Target agent completes work and updates status
- [ ] Delegating agent verifies completion and quality
- [ ] Update DELEGATION.md with final status
- [ ] Close delegation and document lessons learned
- [ ] Update memory files with delegation outcome

## Procedure 7: Code/Documentation Review

**Frequency:** Before deployment or major release
**Owner:** Designated reviewer agent or administrator
**Duration:** 30-60 minutes
**Dependencies:** Code or documentation to review, review criteria

**Checklist:**

- [ ] Identify scope of review (files, components, documents)
- [ ] Confirm review criteria and standards
- [ ] Read and understand the changes
- [ ] Check against style guides and standards
- [ ] Identify bugs, logical issues, or inconsistencies
- [ ] Verify documentation matches implementation
- [ ] Test critical paths if applicable
- [ ] Document all findings (issues, suggestions, approvals)
- [ ] Create issue list if problems found
- [ ] Author responds to feedback
- [ ] Re-review if major changes made
- [ ] Approve or reject with clear rationale
- [ ] Archive review notes
- [ ] Close review ticket

## Procedure 8: Deployment Checklist

**Frequency:** Before production deployment
**Owner:** DevOps or designated administrator
**Duration:** 15-45 minutes (varies by system)
**Dependencies:** Code/config to deploy, deployment credentials

**Checklist:**

- [ ] Create deployment plan (what, when, rollback)
- [ ] Identify stakeholders and notify them
- [ ] Backup current production state
- [ ] Prepare rollback instructions
- [ ] Stage deployment to test environment first
- [ ] Verify test environment functions correctly
- [ ] Run smoke tests on critical features
- [ ] Review logs for errors
- [ ] Proceed to production (or abort)
- [ ] Monitor logs during deployment
- [ ] Verify production health (performance, errors)
- [ ] Run post-deployment smoke tests
- [ ] Confirm with stakeholders deployment succeeded
- [ ] Document deployment with timestamp and changes
- [ ] Archive deployment plan and logs

## Procedure 9: Monitoring and Alerting

**Frequency:** Continuous, with periodic reviews
**Owner:** Agent with monitoring responsibilities
**Duration:** 10-20 minutes per check
**Dependencies:** Monitoring configuration, alert channels

**Checklist:**

- [ ] Check agent error logs for new issues
- [ ] Review task completion rates (success vs. failure)
- [ ] Verify all agents are responding normally
- [ ] Check resource utilization (if applicable)
- [ ] Review response times for time-sensitive operations
- [ ] Identify patterns in failures or slowdowns
- [ ] Check for any manual alerts or escalations
- [ ] Document monitoring findings in daily log
- [ ] Escalate any critical issues immediately
- [ ] Plan investigation or mitigation for detected problems
- [ ] Update monitoring configuration if needed
- [ ] Archive monitoring reports periodically

## Procedure 10: Incident Response

**Frequency:** On demand (when incident occurs)
**Owner:** Administrator, with agent support
**Duration:** 30 minutes - hours (depends on severity)
**Dependencies:** Incident response plan, communication channels

**Checklist:**

- [ ] Declare incident and activate response team
- [ ] Document incident discovery time and impact
- [ ] Identify incident severity (critical/major/minor)
- [ ] Gather immediate logs and context
- [ ] Establish communication channel for response
- [ ] Identify root cause
- [ ] Implement immediate mitigation if possible
- [ ] Communicate impact to stakeholders
- [ ] Implement temporary workaround or fix
- [ ] Test fix in safe environment first
- [ ] Deploy fix to production with monitoring
- [ ] Verify incident is resolved
- [ ] Stand down incident response
- [ ] Conduct post-incident review (within 24-48 hours)
- [ ] Document root cause analysis
- [ ] Create prevention plan for future

## Procedure 11: Quarterly Review and Planning

**Frequency:** Once per quarter
**Owner:** Administrator with agent input
**Duration:** 60-90 minutes
**Dependencies:** Agent memory files, task history, org strategy

**Checklist:**

- [ ] Review agent's performance over past quarter
- [ ] Analyze completed tasks and outcomes
- [ ] Identify what worked well
- [ ] Identify what could improve
- [ ] Gather feedback from stakeholders
- [ ] Review agent's long-term memory (MEMORY.md)
- [ ] Update agent's identity and scope if needed
- [ ] Plan focus areas for next quarter
- [ ] Identify skill gaps or training needs
- [ ] Update GOVERNANCE.md and PROCEDURES.md if needed
- [ ] Set quarterly objectives and key results (if applicable)
- [ ] Schedule regular check-in cadence
- [ ] Document review in workspace history
- [ ] Communicate plan to agent clearly
- [ ] Archive quarterly review document

## Procedure 12: Documentation Updates

**Frequency:** Monthly or as procedures change
**Owner:** Any agent or administrator
**Duration:** 20-40 minutes
**Dependencies:** Current documentation, GOVERNANCE.md, PROCEDURES.md

**Checklist:**

- [ ] Identify documentation that needs updating
- [ ] Review current version and compare to reality
- [ ] Make necessary changes
- [ ] Check for typos, unclear language, outdated references
- [ ] Add examples or clarifications if needed
- [ ] Verify procedures still match current workflow
- [ ] Update version number or last-updated date
- [ ] Test procedures if applicable (dry run)
- [ ] Get feedback from agents using the docs
- [ ] Incorporate feedback
- [ ] Archive previous version
- [ ] Communicate changes to relevant agents
- [ ] Ensure new agents see updated docs

## Procedure 13: Access Control Audit

**Frequency:** Monthly
**Owner:** Administrator
**Duration:** 15-30 minutes
**Dependencies:** Access control system, agent list

**Checklist:**

- [ ] List all active agents and their access levels
- [ ] Verify each agent has appropriate access (not over-provisioned)
- [ ] Identify any unused or deprecated agent accounts
- [ ] Check for shared credentials or keys (should be individual)
- [ ] Review recent access logs for unusual activity
- [ ] Verify no agents have access to inappropriate resources
- [ ] Remove access for agents no longer in workspace
- [ ] Audit backup and recovery credentials
- [ ] Document audit findings
- [ ] Address any access issues found
- [ ] Archive audit report
- [ ] Schedule next audit (30 days)

## Procedure 14: Continuous Improvement

**Frequency:** Ongoing, with periodic reviews
**Owner:** All agents and administrators
**Duration:** Varies
**Dependencies:** Feedback channels, retrospectives

**Checklist:**

- [ ] Encourage agents to suggest improvements
- [ ] Collect feedback from team members working with agents
- [ ] Track improvement ideas in a backlog
- [ ] Prioritize improvements by impact and effort
- [ ] Assign improvement work to qualified agents
- [ ] Implement improvements in test environment first
- [ ] Gather feedback on improvements
- [ ] Deploy successful improvements
- [ ] Communicate changes to all relevant parties
- [ ] Update documentation with improvements
- [ ] Celebrate wins and thank contributors
- [ ] Archive improvement history
- [ ] Use insights to refine next quarter's plan

## How to Use These Procedures

1. **Select relevant procedures** for your workspace based on your needs
2. **Customize checklists** — add, remove, or reorder items to match your workflow
3. **Assign owners** — identify who performs each procedure (agent, admin, team)
4. **Set frequency** — adjust how often procedures run based on your pace
5. **Document locally** — create procedure-specific checklists in your workspace
6. **Review quarterly** — assess which procedures are working and update accordingly
7. **Share learning** — when you improve a procedure, update this document for future teams

## Integration with Governance and Delegation

- **GOVERNANCE.md** provides the daily behavior standards agents follow
- **PROCEDURES.md** (this doc) provides structured operations agents execute
- **DELEGATION.md** provides protocols when agents work together across tasks

Together, these three documents form a complete operational framework.
