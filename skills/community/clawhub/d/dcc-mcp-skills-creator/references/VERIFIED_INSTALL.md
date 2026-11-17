# Install a reviewed Skill revision

Use a trusted, already installed Git and tar. Obtain the full 40-character
commit ID from your independently trusted code-review record for
`dcc-mcp/dcc-mcp-agent-plugins`. Review that revision's Skill instructions,
scripts, and version before authorizing installation. Do not derive the trust
pin by resolving `main`, `latest`, or a tag at installation time.

Run this Bash procedure in an empty staging directory outside every agent's
Skill discovery paths. Replace the placeholder with the reviewed commit ID.
The placeholder fails before any network access. Git checks downloaded object
identities, and `fsck` validates the retrieved object graph before export.

```bash
set -euo pipefail
reviewed_commit='REPLACE_WITH_REVIEWED_40_CHARACTER_COMMIT_ID'
[[ "$reviewed_commit" =~ ^[0-9a-f]{40}$ ]] || { echo 'A reviewed full commit ID is required' >&2; exit 1; }
mkdir skill-source
git -C skill-source init --bare
git -C skill-source -c fetch.fsckObjects=true fetch --depth=1 \
  https://github.com/dcc-mcp/dcc-mcp-agent-plugins.git "$reviewed_commit"
test "$(git -C skill-source rev-parse 'FETCH_HEAD^{commit}')" = "$reviewed_commit"
git -C skill-source fsck --strict
git -C skill-source -c core.autocrlf=false archive --format=tar --output=../reviewed-skill.tar \
  "$reviewed_commit:plugins/dcc-mcp/skills/dcc-mcp-skills-creator"
mkdir dcc-mcp-skills-creator
tar -xf reviewed-skill.tar -C dcc-mcp-skills-creator
```

Stop on any error; never fall back to a registry or another revision. The
export is addressed by the reviewed Git commit and its tree/blob hashes.
This verifies content identity against that pin, not publisher signatures or
the safety of the reviewed code. A pin from a compromised source is not a
trustworthy review record.

Confirm `metadata.dcc-mcp.version` in the exported `SKILL.md` matches your
review record, then move the exported directory into the chosen agent's
documented Skill directory. Do not overwrite an existing installation. Retain
the commit ID and archive with the review record so later installations use
the same bytes. Load the Skill only after this verification; install its
runtime prerequisites separately under their own reviewed procedure.
