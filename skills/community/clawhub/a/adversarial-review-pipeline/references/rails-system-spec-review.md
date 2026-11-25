# Rails System Spec Review

Writing tests from the user's perspective, and the Rails journeys worth walking.

## The System Spec Writer in a Rails review

Writing tests from the user's perspective, without reading the controller
first, is what catches the browser-only bugs. The discipline matters:

**Do not read the controller before writing the spec.** Write the spec from
"what does the user do". Then run it. If it passes, the code matches the
journey. If it fails, the red spec tells you which of the two is wrong -
and the spec is usually right, because it was written from the requirement
rather than from the implementation.

The red-then-green loop: write the spec, run it, make the smallest production
change to go green, run it again.

This catches things a controller-reading reviewer cannot, because a reviewer
who has read the controller already "knows" what the code does and will
accept it.

### Two phases, in order

1. **User-journey specs.** Cover the journeys the change is about, from the
   user's perspective.
2. **QA edge-case sweep.** After the journey specs are green, review the
   findings and the existing specs for missed edges: empty states, boundary
   values, permission boundaries, Turbo and redirect edge cases, error paths,
   lifecycle gaps. Add coverage **only where necessary** - prefer a model or
   request spec when the edge is not user-visible.

### Rails-specific journey checklist

For each journey, verify the real browser path:

- [ ] The form submits with the payload the browser actually sends - not a
      synthetic shape the spec invented to satisfy a guard.
- [ ] The redirect target is reachable and does not leave the user in a frame
      that cannot render the response.
- [ ] Validation errors render back into the form with the submitted values
      intact.
- [ ] Authorization is checked on the way in, and the unauthorized path
      returns the right response rather than a 500.
- [ ] A second submission of the same form does not create a duplicate.
- [ ] The user can leave the page - sign out, cancel, back - from every state
      the flow can reach.

---
