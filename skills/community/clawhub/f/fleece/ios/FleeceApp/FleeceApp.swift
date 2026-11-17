import SwiftUI
import AppIntents

@main
struct FleeceApp: App {

    init() {
        FleeceShortcuts.updateAppShortcutParameters()
    }


    @StateObject private var appState           = AppState()
    @StateObject private var locationManager    = LocationManager()
    @StateObject private var notificationManager = NotificationManager()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(appState)
                .environmentObject(locationManager)
                .environmentObject(notificationManager)
                .task {
                    notificationManager.registerActionCategory()
                    await notificationManager.requestPermission()
                    locationManager.requestPermission()
                }
                .onChange(of: locationManager.coordinate) { _, coord in
                    guard let coord else { return }
                    appState.onLocationUpdate(coord,
                                              notificationManager: notificationManager)
                }
                .onOpenURL { url in
                    switch url.host {
                    case "wallet":   appState.selectedTab = .wallet
                    case "ask":      appState.selectedTab = .ask
                    case "settings": appState.selectedTab = .settings
                    default:         appState.selectedTab = .home
                    }
                }
        }
    }
}
