# Agent and workflow failures

Follow the actual trajectory for the affected run: user request, retrieved evidence, model decisions, tool arguments and results, handoffs, retries and final output. Preserve nested errors and original values where they determine what happened; sanitize private content before external research.

Find the first consequential divergence from the task or component contract. A final wrapper error may follow an earlier ignored result, incorrect parameter, wrong target or lossy handoff. Distinguish a missing event from an event not captured by the available recorder.

A source quotation supports that an observation exists; it does not establish the observation caused the failure. Test the proposed causal link with a focused replay or other safe check when possible. Reuse unchanged successful stages and preserve external side effects rather than rerunning the entire workflow.

Consult authorized existing incident records for their trigger, applicable version, successful verification, failed remedies and exclusions. Save a new record only when requested or within an already authorized recording workflow. Do not create global memory or alter the agent's standing instructions.
