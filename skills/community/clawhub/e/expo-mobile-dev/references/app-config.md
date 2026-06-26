# `app.config.ts` Patterns

Static `app.json` works fine for small apps. Switch to `app.config.ts` when you need any of:

- Environment variables driving the config
- Different bundle IDs / names per build profile (e.g., dev vs prod app on the same device)
- Conditional plugins
- Build-time computed values

When both `app.json` and `app.config.ts` exist, `app.config.ts` wins and can spread the JSON file in.

## Basic template

```ts
import type { ExpoConfig, ConfigContext } from 'expo/config';

export default ({ config }: ConfigContext): ExpoConfig => {
  const variant = process.env.APP_VARIANT ?? 'production';
  const isDev = variant === 'development';

  return {
    ...config,
    name: isDev ? 'MyApp (Dev)' : 'MyApp',
    slug: 'my-app',
    scheme: 'myapp',
    version: '1.0.0',
    orientation: 'portrait',
    icon: './assets/icon.png',
    userInterfaceStyle: 'automatic',
    newArchEnabled: true,

    ios: {
      bundleIdentifier: isDev ? 'com.example.myapp.dev' : 'com.example.myapp',
      supportsTablet: true,
      infoPlist: {
        NSCameraUsageDescription: 'Take photos for your profile.',
        NSLocationWhenInUseUsageDescription: 'Show nearby content.',
      },
    },

    android: {
      package: isDev ? 'com.example.myapp.dev' : 'com.example.myapp',
      adaptiveIcon: {
        foregroundImage: './assets/adaptive-icon.png',
        backgroundColor: '#ffffff',
      },
      permissions: ['CAMERA', 'ACCESS_FINE_LOCATION'],
    },

    plugins: [
      'expo-router',
      'expo-secure-store',
      ['expo-camera', { cameraPermission: 'Allow $(PRODUCT_NAME) to access your camera.' }],
    ],

    extra: {
      apiUrl: process.env.EXPO_PUBLIC_API_URL,
      eas: { projectId: 'your-eas-project-id' },
    },
  };
};
```

## Different app variants on the same device

This is the killer feature of `app.config.ts`: install dev, preview, and production builds side-by-side without overwriting each other.

```ts
const variant = process.env.APP_VARIANT;
const bundleId = {
  development: 'com.example.myapp.dev',
  preview: 'com.example.myapp.preview',
  production: 'com.example.myapp',
}[variant ?? 'production'];
```

Then in `eas.json`:

```json
{
  "build": {
    "development": { "env": { "APP_VARIANT": "development" }, "developmentClient": true },
    "preview":     { "env": { "APP_VARIANT": "preview" } },
    "production":  { "env": { "APP_VARIANT": "production" } }
  }
}
```

## Reading env vars in app code

Two paths:

1. **`EXPO_PUBLIC_*` env vars** are inlined at build time and accessible as `process.env.EXPO_PUBLIC_API_URL` from any file. Use for non-secrets.
2. **`extra` block** — set values in `app.config.ts` then read via `Constants.expoConfig?.extra?.apiUrl` from `expo-constants`. Use for values computed in the config or shared across env-var and static sources.

Never put secrets (API keys for backends that should authenticate) in the JS bundle. Anything shipped to the client is readable. Put backend secrets in your server, not the app.

## Plugins

Most native config that used to require editing `Info.plist` / `AndroidManifest.xml` is now handled by config plugins:

```ts
plugins: [
  // Simple plugin (no config)
  'expo-secure-store',

  // Plugin with config — array form
  ['expo-build-properties', {
    ios: { deploymentTarget: '15.1' },
    android: { compileSdkVersion: 34 },
  }],

  // Permission text customization
  ['expo-camera', { cameraPermission: 'We need camera access to scan QR codes.' }],
],
```

When a community library tells you to "add this to Info.plist", check first if it ships a config plugin — it usually does.

## When `app.config.ts` isn't enough

If you find yourself wanting to write a custom config plugin, see [Expo's config plugin docs](https://docs.expo.dev/config-plugins/introduction/). Common cases:

- Adding entries to `Info.plist` that no library exposes
- Modifying `AndroidManifest.xml` (e.g., custom intent filters)
- Running scripts at prebuild time

Custom plugins live as files in your repo and get referenced in the `plugins` array. They keep you from having to eject.
