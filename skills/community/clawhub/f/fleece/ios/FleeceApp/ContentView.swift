import SwiftUI

struct ContentView: View {
    @EnvironmentObject var appState: AppState
    @EnvironmentObject var locationManager: LocationManager
    @AppStorage("colorScheme") private var schemePref: String = "system"

    private var preferredColorScheme: ColorScheme? {
        switch schemePref {
        case "light": return .light
        case "dark":  return .dark
        default:      return nil
        }
    }

    var body: some View {
        TabView(selection: $appState.selectedTab) {
            HomeView()
                .tabItem { Label("Nearby", systemImage: "location.fill") }
                .tag(AppState.Tab.home)

            WalletView()
                .tabItem { Label("Wallet", systemImage: "creditcard.fill") }
                .tag(AppState.Tab.wallet)

            AskView()
                .tabItem { Label("Ask", systemImage: "bubble.left.and.bubble.right.fill") }
                .tag(AppState.Tab.ask)

            SettingsView()
                .tabItem { Label("Settings", systemImage: "gear") }
                .tag(AppState.Tab.settings)
        }
        .tint(.indigo)
        .preferredColorScheme(preferredColorScheme)
        .sheet(isPresented: $appState.showRecommendationSheet) {
            if let place = appState.currentPlace {
                RecommendationsSheetView(
                    place: place,
                    recommendations: appState.recommendations
                )
            }
        }
    }
}
