---
name: fe-cli-rn
description: >
  Scaffold a React Native mobile application. For iOS/Android native mobile apps.
  Uses Expo (recommended) or React Native CLI. Features navigation, state management, theming.
  Triggered as a sub-skill of fe-cli when user wants React Native/RN/原生移动/App project.
---

# fe-cli-rn — React Native Mobile App Scaffolding

## Workflow

### Step 1: Gather Options

1. **Approach**: Expo (recommended, faster setup) / React Native CLI (more native control)
2. **Navigation**: Expo Router (file-based, recommended) / React Navigation (component-based)
3. **Styling**: NativeWind (Tailwind for RN) / StyleSheet / Tamagui / React Native Paper
4. **State Management**: Zustand / Redux Toolkit / None
5. **i18n**: i18next + react-i18next / None
6. **Testing**: Jest + React Native Testing Library / None
7. **Pre-commit**: husky + lint-staged? (default: No)
8. **Project name**: string

**Expo vs CLI:**
- **Expo**: Faster dev, OTA updates, easy build (EAS), limited native modules (improving)
- **CLI**: Full native control, custom native modules, more complex setup

### Step 2: Scaffold

**Expo (recommended):**
```
bunx create-expo-app <project-name> --template tabs
```

Templates: `blank` / `tabs` / `minimal` / `expo-template-blank-typescript`

**React Native CLI:**
```
bunx react-native init <project-name> --template react-native-template-typescript
```

### Step 3: Install Additional Dependencies

| Selection | Packages |
|---|---|
| Expo Router | `npx expo install expo-router react-native-safe-area-context react-native-screens expo-linking expo-constants expo-status-bar` |
| React Navigation | `@react-navigation/native @react-navigation/native-stack @react-navigation/bottom-tabs react-native-screens react-native-safe-area-context` |
| NativeWind | `npx expo install nativewind tailwindcss` + `tailwind.config.js` |
| Tamagui | `@tamagui/core @tamagui/config` |
| React Native Paper | `react-native-paper` |
| Zustand | `zustand` |
| Redux Toolkit | `@reduxjs/toolkit react-redux` |
| i18n | `i18next react-i18next` |
| Animations | `react-native-reanimated` |
| Gesture | `react-native-gesture-handler` |
| Charts | `react-native-svg victor-native` / `react-native-chart-kit` |
| Storage | `@react-native-async-storage/async-storage` |
| Image | `expo-image` |
| Font | `expo-font` |

### Step 4: Project Structure

**Expo + Expo Router:**
```
project-name/
├── app/                        # File-based routing (Expo Router)
│   ├── _layout.tsx             # Root layout
│   ├── index.tsx               # Home screen
│   ├── (tabs)/                 # Tab navigation group
│   │   ├── _layout.tsx         # Tab layout
│   │   ├── index.tsx           # Tab: Home
│   │   ├── explore.tsx         # Tab: Explore
│   │   └── profile.tsx         # Tab: Profile
│   └── modal.tsx               # Modal screen
├── components/
│   ├── ThemedView.tsx          # Themed container
│   ├── ThemedText.tsx          # Themed text
│   └── LoadingScreen.tsx       # Loading state
├── hooks/
│   ├── useTheme.ts             # Theme hook
│   └── useRequest.ts           # Data fetching
├── stores/
│   └── appStore.ts             # Zustand store
├── services/
│   ├── request.ts              # API client
│   └── api/
│       └── index.ts            # API endpoints
├── constants/
│   └── theme.ts                # Colors, spacing, typography
├── assets/                     # Images, fonts
├── app.json                    # Expo config
├── app.config.ts               # Expo config (TypeScript)
├── tsconfig.json
└── package.json
```

**React Native CLI + React Navigation:**
```
project-name/
├── src/
│   ├── screens/
│   │   ├── HomeScreen.tsx
│   │   ├── DetailScreen.tsx
│   │   └── ProfileScreen.tsx
│   ├── navigation/
│   │   ├── AppNavigator.tsx     # Root navigator
│   │   ├── TabNavigator.tsx     # Bottom tabs
│   │   └── types.ts             # Navigation types
│   ├── components/
│   ├── hooks/
│   ├── stores/
│   ├── services/
│   └── constants/
├── android/                     # Native Android
├── ios/                         # Native iOS
├── index.js                     # Entry point
├── App.tsx                      # Root component
└── package.json
```

### Step 5: Key Templates

**`app/_layout.tsx`** (Expo Router root):
```tsx
import { Stack } from 'expo-router';

export default function RootLayout() {
  return (
    <Stack>
      <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
      <Stack.Screen name="modal" options={{ presentation: 'modal' }} />
    </Stack>
  );
}
```

**`app/(tabs)/_layout.tsx`** (Tab layout):
```tsx
import { Tabs } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

export default function TabLayout() {
  return (
    <Tabs screenOptions={{ tabBarActiveTintColor: '#1677ff' }}>
      <Tabs.Screen
        name="index"
        options={{ title: 'Home', tabBarIcon: ({ color, size }) => <Ionicons name="home" size={size} color={color} /> }}
      />
      <Tabs.Screen
        name="explore"
        options={{ title: 'Explore', tabBarIcon: ({ color, size }) => <Ionicons name="search" size={size} color={color} /> }}
      />
      <Tabs.Screen
        name="profile"
        options={{ title: 'Profile', tabBarIcon: ({ color, size }) => <Ionicons name="person" size={size} color={color} /> }}
      />
    </Tabs>
  );
}
```

**`constants/theme.ts`:**
```typescript
export const Colors = {
  light: {
    primary: '#1677ff',
    background: '#ffffff',
    text: '#1a1a1a',
    textSecondary: '#666666',
    border: '#e8e8e8',
    card: '#f5f5f5',
    error: '#ff4d4f',
    success: '#52c41a',
  },
  dark: {
    primary: '#4096ff',
    background: '#1a1a1a',
    text: '#ffffff',
    textSecondary: '#999999',
    border: '#333333',
    card: '#2a2a2a',
    error: '#ff7875',
    success: '#73d13d',
  },
};

export const Spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
};

export const Typography = {
  h1: { fontSize: 28, fontWeight: '700' as const },
  h2: { fontSize: 22, fontWeight: '600' as const },
  h3: { fontSize: 18, fontWeight: '600' as const },
  body: { fontSize: 16, fontWeight: '400' as const },
  caption: { fontSize: 13, fontWeight: '400' as const },
};
```

**`app.config.ts`** (Expo config):
```typescript
import { ExpoConfig, ConfigContext } from 'expo/config';

export default ({ config }: ConfigContext): ExpoConfig => ({
  ...config,
  name: 'Your App',
  slug: 'your-app',
  version: '1.0.0',
  orientation: 'portrait',
  scheme: 'yourapp',
  userInterfaceStyle: 'automatic',
  newArchEnabled: true,
  ios: {
    supportsTablet: true,
    bundleIdentifier: 'com.example.app',
  },
  android: {
    adaptiveIcon: { backgroundColor: '#ffffff' },
    package: 'com.example.app',
  },
  plugins: ['expo-router', 'expo-font'],
});
```

### Step 6: Final Setup

```bash
cd <project-name>
bun install
bun start      # Expo: starts Metro bundler
# Press 'i' for iOS simulator, 'a' for Android emulator
```

**EAS Build** (Expo cloud build):
```bash
bun add -g eas-cli
eas login
eas build:configure
eas build --platform ios     # or android / all
```

**Local build:**
```bash
# iOS (requires macOS + Xcode)
npx expo run:ios

# Android (requires Android Studio)
npx expo run:android
```

Announce: React Native project ready with Expo, navigation, and theming. Dev server at Expo Go or simulator.
