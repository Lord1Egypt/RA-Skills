# Performance and Accessibility - Animate

Animation is only good if it survives real devices and accessibility settings.

## Safe Defaults

Prefer:
- `transform`
- `opacity`
- carefully controlled color changes
- stack-native layout animation primitives when layout must move

Avoid by default:
- width and height tweens
- top and left movement
- blur-heavy or shadow-heavy loops
- infinite motion without pause or clear purpose

## Interruption Checklist

Define behavior for:
- repeated taps
- swipe back or dismiss
- route change during animation
- async completion before animation ends
- unmount or offscreen transitions

If interruption is undefined, the motion is not ready.

## Reduced Motion

Always support the platform setting:
- Web: `prefers-reduced-motion`
- iOS and SwiftUI: Reduce Motion
- Android and Compose: system animator duration scale
- React Native: platform accessibility setting
- Flutter: app and platform animation disable signals

Fallback strategy:
- reduce travel distance
- shorten duration
- remove parallax, bounce, and ornamental loops
- keep meaning through opacity, color, or instant state confirmation

## Low-End Device Strategy

When the surface is heavy:
- drop blur and layered shadows first
- simplify stagger depth
- reduce simultaneous moving elements
- prefer one strong animation over many weak ones

## Screen Reader and Focus Safety

Motion must not:
- reorder focus unpredictably
- hide state changes from assistive tech
- require vision-only interpretation of success or error

State change semantics still need text, labels, and announcements.
