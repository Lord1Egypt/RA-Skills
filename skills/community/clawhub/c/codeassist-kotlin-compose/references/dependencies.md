# Available Dependencies

These are the ONLY dependencies available in CodeAssist. Do NOT add any others to module.toml.

## Direct Dependencies

| Dependency | Version | Purpose |
|---|---|---|
| `kotlin-stdlib` | 2.4.0 | Kotlin standard library |
| `androidx.activity:activity-compose` | 1.9.3 | ComponentActivity + setContent {} |
| `androidx.compose.ui:ui` | 1.7.5 | Core Compose UI framework |
| `androidx.compose.foundation:foundation` | 1.7.5 | Layout, lazy lists, gestures, shapes, scroll |
| `androidx.compose.material3:material3` | 1.3.1 | Material 3 components (Button, Card, TextField, TopAppBar, etc.) |
| `androidx.compose.ui:ui-tooling-preview` | 1.7.5 | @Preview annotation support |

## Transitive Dependencies (available automatically)

| Package | Version | Key Classes |
|---|---|---|
| `kotlinx.coroutines.android` | 1.7.3 | `Dispatchers.Main`, `lifecycleScope` |
| `kotlinx.coroutines.core` | 1.7.3 | `launch`, `async`, `flow`, `delay` |
| `androidx.lifecycle:lifecycle-runtime` | 2.8.3 | `lifecycleScope`, `repeatOnLifecycle` |
| `androidx.lifecycle:lifecycle-viewmodel` | 2.8.3 | `ViewModel`, `viewModelScope` |
| `androidx.lifecycle:lifecycle-runtime-compose` | 2.8.3 | `collectAsStateWithLifecycle()` |
| `androidx.lifecycle:lifecycle-viewmodel-compose` | 2.8.3 | `viewModel()` composable |
| `androidx.core:core-ktx` | 1.13.0 | Kotlin extensions for Android |
| `androidx.compose.animation` | 1.7.5 | `AnimatedVisibility`, `Crossfade`, `animateContentSize` |
| `androidx.compose.material:material-icons-core` | 1.6.0 | `Icons.Default.*`, `Icons.Outlined.*` |
| `androidx.annotation` | 1.8.1 | `@StringRes`, `@DrawableRes`, etc. |

## Common Import Patterns

```kotlin
// Activity & Compose entry
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent

// Compose UI
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material.icons.outlined.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

// Animation
import androidx.compose.animation.*
import androidx.compose.animation.core.*

// Coroutines
import kotlinx.coroutines.*

// Lifecycle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewmodel.compose.viewModel
```

## NOT Available (NEVER use these)

- `androidx.navigation:navigation-compose` — NO navigation library
- `androidx.room:room-*` — NO Room database
- `com.squareup.retrofit2:*` — NO Retrofit
- `com.squareup.okhttp3:*` — NO OkHttp
- `io.coil-kt:*` — NO Coil image loading
- `com.github.bumptech.glide:*` — NO Glide
- `com.google.dagger:*` — NO Dagger/Hilt
- `com.google.accompanist:*` — NO Accompanist
- `androidx.datastore:*` — NO DataStore
- `com.google.code.gson:*` — NO Gson (use kotlinx.serialization or manual JSON)
- `org.jetbrains.kotlinx:kotlinx-serialization-*` — NO kotlinx-serialization

## Navigation Pattern (without Navigation library)

Since Navigation Compose is NOT available, use state-based navigation:

```kotlin
enum class Screen { Home, Detail, Settings }

@Composable
fun AppNavigation() {
    var currentScreen by remember { mutableStateOf(Screen.Home) }

    when (currentScreen) {
        Screen.Home -> HomeScreen(
            onNavigateToDetail = { currentScreen = Screen.Detail },
            onNavigateToSettings = { currentScreen = Screen.Settings }
        )
        Screen.Detail -> DetailScreen(
            onBack = { currentScreen = Screen.Home }
        )
        Screen.Settings -> SettingsScreen(
            onBack = { currentScreen = Screen.Home }
        )
    }
}
```

## Data Persistence (without Room)

Since Room is NOT available, use SharedPreferences for simple data:

```kotlin
val prefs = context.getSharedPreferences("app_prefs", Context.MODE_PRIVATE)
prefs.edit().putString("key", "value").apply()
val value = prefs.getString("key", "default")
```

For more complex data, use JSON files in internal storage:

```kotlin
val file = File(context.filesDir, "data.json")
file.writeText(jsonString)
val data = file.readText()
```

## Networking (without Retrofit/OkHttp)

Use `java.net.HttpURLConnection` or `java.net.URL`:

```kotlin
suspend fun fetchData(url: String): String = withContext(Dispatchers.IO) {
    val connection = java.net.URL(url).openConnection() as java.net.HttpURLConnection
    try {
        connection.requestMethod = "GET"
        connection.inputStream.bufferedReader().readText()
    } finally {
        connection.disconnect()
    }
}
```
