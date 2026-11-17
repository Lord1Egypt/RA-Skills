# Polish — Final Quality Pass

`polish` is the last review before the interface is considered ready. It is not a loop. Do one batch of fixes and one final check.

## Checklist

### Visual

- [ ] No generic or AI-generated tells (see [anti-patterns.md](anti-patterns.md)).
- [ ] Color palette is harmonious and accessible.
- [ ] Typography has clear hierarchy and readable measures.
- [ ] Spacing follows the 8px or 4px scale.
- [ ] Alignment is intentional and consistent.

### Responsive

- [ ] Mobile view at 375px is the strongest story.
- [ ] Layout shifts are meaningful at each breakpoint.
- [ ] Touch targets are large enough on small screens.
- [ ] Images and media do not overflow or distort.

### Interaction

- [ ] Hover, focus, active, and disabled states are defined.
- [ ] Loading, empty, and error states are designed.
- [ ] Motion is purposeful and has a reduced-motion fallback.
- [ ] Forms are usable with keyboard and screen reader.

### Framework

- [ ] Component boundaries match the target framework's conventions.
- [ ] Design tokens are implemented consistently.
- [ ] No framework defaults are passed off as brand design.

## Stop Condition

Stop after the second full pass. Additional rounds usually introduce noise, not quality.
