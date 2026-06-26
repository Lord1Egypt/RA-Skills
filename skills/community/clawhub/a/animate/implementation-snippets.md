# Implementation Snippets - Animate

Use these as starter shapes, then adapt them to the real state model and interruption rules.

## Flutter

```dart
AnimatedSwitcher(
  duration: const Duration(milliseconds: 220),
  child: isLoading
      ? const CircularProgressIndicator()
      : const Icon(Icons.check, key: ValueKey('done')),
)
```

## React

```tsx
<AnimatePresence mode="wait">
  {isOpen && (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} />
  )}
</AnimatePresence>
```

## SwiftUI

```swift
withAnimation(.easeOut(duration: 0.22)) {
  isExpanded.toggle()
}
```

## Jetpack Compose

```kotlin
AnimatedVisibility(
  visible = isVisible,
  enter = fadeIn() + slideInVertically(),
  exit = fadeOut() + slideOutVertically()
) { SheetBody() }
```

## React Native

```tsx
Animated.timing(opacity, {
  toValue: isVisible ? 1 : 0,
  duration: 220,
  useNativeDriver: true,
}).start();
```

## Web

```css
.card {
  transition: transform 220ms ease, opacity 220ms ease;
}
.card[data-state='open'] { transform: translateY(0); opacity: 1; }
```
