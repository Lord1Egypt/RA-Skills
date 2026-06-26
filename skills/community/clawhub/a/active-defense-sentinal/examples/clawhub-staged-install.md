# Example: ClawHub Staged Install

A user requests installation of a ClawHub skill by slug.

Expected behavior:
- stage the install in the workspace
- scan the staged copy before exposure
- install only if the scan is safe or warning-only
- block High/Critical before the skill becomes active