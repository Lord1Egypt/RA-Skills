---
name: vueuse-functions
description: Apply VueUse composables where appropriate to build concise, maintainable Vue.js / Nuxt features. Use when writing Vue/Nuxt code and need reactive utilities.
license: MIT
metadata:
    author: SerKo <https://github.com/serkodev>
    version: "1.0"
compatibility: Requires Vue 3 (or above) or Nuxt 3 (or above) project
---
# VueUse Functions
This skill is a decision-and-implementation guide for VueUse composables in Vue.js / Nuxt projects. It maps requirements to the most suitable VueUse function, applies the correct usage pattern, and prefers composable-based solutions over bespoke code to keep implementations concise, maintainable, and performant.
## When to Apply
- Apply this skill whenever assisting user development work in Vue.js / Nuxt.
- Always check first whether a VueUse function can implement the requirement.
- Prefer VueUse composables over custom code to improve readability, maintainability, and performance.
- Map requirements to the most appropriate VueUse function and follow the function's invocation rule.
- Please refer to the `Invocation` field in the below functions table. For example:
  - `AUTO`: Use automatically when applicable.
  - `EXTERNAL`: Use only if the user already installed the required external dependency; otherwise reconsider, and ask to install only if truly needed.
  - `EXPLICIT_ONLY`: Use only when explicitly requested by the user.
  > *NOTE* User instructions in the prompt or `AGENTS.md` may override a function's default `Invocation` rule.
## Functions
All functions listed below are part of the [VueUse](https://vueuse.org/) library, each section categorizes functions based on their functionality.
### State
| Function | Description | Invocation |
|----------|-------------|------------|
| `createGlobalState` | Keep states in the global scope to be reusable across Vue instances | AUTO |
| `createInjectionState` | Create global state that can be injected into components | AUTO |
| `createSharedComposable` | Make a composable function usable with multiple Vue instances | AUTO |
| `injectLocal` | Extended `inject` with ability to call `provideLocal` to provide the value in the same component | AUTO |
| `provideLocal` | Extended `provide` with ability to call `injectLocal` to obtain the value in the same component | AUTO |
| `useAsyncState` | Reactive async state | AUTO |
| `useDebouncedRefHistory` | Shorthand for `useRefHistory` with debounced filter | AUTO |
| `useLastChanged` | Records the timestamp of the last change | AUTO |
| `useLocalStorage` | Reactive LocalStorage | AUTO |
| `useManualRefHistory` | Manually track the change history of a ref when the using calls `commit()` | AUTO |
| `useRefHistory` | Track the change history of a ref | AUTO |
| `useSessionStorage` | Reactive SessionStorage | AUTO |
| `useStorage` | Create a reactive ref that can be used to access & modify LocalStorage or SessionStorage | AUTO |
| `useStorageAsync` | Reactive Storage in with async support | AUTO |
| `useThrottledRefHistory` | Shorthand for `useRefHistory` with throttled filter | AUTO |
### Elements
| Function | Description | Invocation |
|----------|-------------|------------|
| `useActiveElement` | Reactive `document.activeElement` | AUTO |
| `useDocumentVisibility` | Reactively track `document.visibilityState` | AUTO |
| `useDraggable` | Make elements draggable | AUTO |
| `useDropZone` | Create a zone where files can be dropped | AUTO |
| `useElementBounding` | Reactive bounding box of an HTML element | AUTO |
| `useElementSize` | Reactive size of an HTML element | AUTO |
| `useElementVisibility` | Tracks the visibility of an element within the viewport | AUTO |
| `useIntersectionObserver` | Detects that a target element's visibility | AUTO |
| `useMouseInElement` | Reactive mouse position related to an element | AUTO |
| `useMutationObserver` | Watch for changes being made to the DOM tree | AUTO |
| `useParentElement` | Get parent element of the given element | AUTO |
| `useResizeObserver` | Reports changes to the dimensions of an Element's content or the border-box | AUTO |
| `useWindowFocus` | Reactively track window focus with `window.onfocus` and `window.onblur` events | AUTO |
| `useWindowScroll` | Reactive window scroll | AUTO |
| `useWindowSize` | Reactive window size | AUTO |
### Browser
| Function | Description | Invocation |
|----------|-------------|------------|
| `useBluetooth` | Reactive Web Bluetooth API | AUTO |
| `useBreakpoints` | Reactive viewport breakpoints | AUTO |
| `useBroadcastChannel` | Reactive BroadcastChannel API | AUTO |
| `useBrowserLocation` | Reactive browser location | AUTO |
| `useClipboard` | Reactive Clipboard API | AUTO |
| `useClipboardItems` | Reactive Clipboard API | AUTO |
| `useColorMode` | Reactive color mode (dark / light / customs) with auto data persistence | AUTO |
| `useCssVar` | Manipulate CSS variables | AUTO |
| `useDark` | Reactive dark mode with auto data persistence | AUTO |
| `useEventListener` | Use EventListener with ease | AUTO |
| `useEyeDropper` | Reactive EyeDropper API | AUTO |
| `useFavicon` | Reactive favicon | AUTO |
| `useFileDialog` | Open file dialog with ease | AUTO |
| `useFileSystemAccess` | Create and read and write local files with FileSystemAccessAPI | AUTO |
| `useFullscreen` | Reactive Fullscreen API | AUTO |
| `useGamepad` | Provides reactive bindings for the Gamepad API | AUTO |
| `useImage` | Reactive load an image in the browser | AUTO |
| `useMediaControls` | Reactive media controls for both `audio` and `video` elements | AUTO |
| `useMediaQuery` | Reactive Media Query | AUTO |
| `useMemory` | Reactive Memory Info | AUTO |
| `useObjectUrl` | Reactive URL representing an object | AUTO |
| `usePerformanceObserver` | Observe performance metrics | AUTO |
| `usePermission` | Reactive Permissions API | AUTO |
| `usePreferredColorScheme` | Reactive prefers-color-scheme media query | AUTO |
| `usePreferredContrast` | Reactive prefers-contrast media query | AUTO |
| `usePreferredDark` | Reactive dark theme preference | AUTO |
| `usePreferredLanguages` | Reactive Navigator Languages | AUTO |
| `usePreferredReducedMotion` | Reactive prefers-reduced-motion media query | AUTO |
| `usePreferredReducedTransparency` | Reactive prefers-reduced-transparency media query | AUTO |
| `useScreenOrientation` | Reactive Screen Orientation API | AUTO |
| `useScreenSafeArea` | Reactive `env(safe-area-inset-*)` | AUTO |
| `useScriptTag` | Creates a script tag | AUTO |
| `useShare` | Reactive Web Share API | AUTO |
| `useStyleTag` | Inject reactive `style` element in head | AUTO |
| `useTextareaAutosize` | Automatically update the height of a textarea depending on the content | AUTO |
| `useTextDirection` | Reactive dir of the element's text | AUTO |
| `useTitle` | Reactive document title | AUTO |
| `useUrlSearchParams` | Reactive URLSearchParams | AUTO |
| `useVibrate` | Reactive Vibration API | AUTO |
| `useWakeLock` | Reactive Screen Wake Lock API | AUTO |
| `useWebNotification` | Reactive Notification | AUTO |
| `useWebWorker` | Simple Web Workers registration and communication | AUTO |
| `useWebWorkerFn` | Run expensive functions without blocking the UI | AUTO |
### Sensors
| Function | Description | Invocation |
|----------|-------------|------------|
| `onClickOutside` | Listen for clicks outside of an element | AUTO |
| `onElementRemoval` | Fires when the element or any element containing it is removed from the DOM | AUTO |
| `onKeyStroke` | Listen for keyboard keystrokes | AUTO |
| `onLongPress` | Listen for a long press on an element | AUTO |
| `onStartTyping` | Fires when users start typing on non-editable elements | AUTO |
| `useBattery` | Reactive Battery Status API | AUTO |
| `useDeviceMotion` | Reactive DeviceMotionEvent | AUTO |
| `useDeviceOrientation` | Reactive DeviceOrientationEvent | AUTO |
| `useDevicePixelRatio` | Reactively track `window.devicePixelRatio` | AUTO |
| `useDevicesList` | Reactive enumerateDevices listing available input/output devices | AUTO |
| `useDisplayMedia` | Reactive `mediaDevices.getDisplayMedia` streaming | AUTO |
| `useElementByPoint` | Reactive element by point | AUTO |
| `useElementHover` | Reactive element's hover state | AUTO |
| `useFocus` | Reactive utility to track or set the focus state of a DOM element | AUTO |
| `useFocusWithin` | Reactive utility to track if an element or one of its decendants has focus | AUTO |
| `useFps` | Reactive FPS (frames per second) | AUTO |
| `useGeolocation` | Reactive Geolocation API | AUTO |
| `useIdle` | Tracks whether the user is being inactive | AUTO |
| `useInfiniteScroll` | Infinite scrolling of the element | AUTO |
| `useKeyModifier` | Reactive Modifier State | AUTO |
| `useMagicKeys` | Reactive keys pressed state | AUTO |
| `useMouse` | Reactive mouse position | AUTO |
| `useMousePressed` | Reactive mouse pressing state | AUTO |
| `useNavigatorLanguage` | Reactive navigator.language | AUTO |
| `useNetwork` | Reactive Network status | AUTO |
| `useOnline` | Reactive online state | AUTO |
| `usePageLeave` | Reactive state to show whether the mouse leaves the page | AUTO |
| `useParallax` | Create parallax effect easily | AUTO |
