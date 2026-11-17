import SwiftUI
import MapKit
import UIKit

struct HomeView: View {
    @EnvironmentObject var appState: AppState
    @EnvironmentObject var locationManager: LocationManager
    @EnvironmentObject var notificationManager: NotificationManager

    @State private var mapPosition: MapCameraPosition = .automatic
    @State private var selectedPlaceID: String?
    @State private var pinnedCoordinate: CLLocationCoordinate2D?

    var body: some View {
        NavigationStack {
            ZStack(alignment: .bottom) {
                mapLayer
                overlayLayer
            }
            .navigationTitle("Fleece")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar { toolbarContent }
            .onChange(of: locationManager.coordinate) { _, newCoord in
                guard let newCoord else { return }
                pinnedCoordinate = nil   // clear manual pin on GPS update
                withAnimation {
                    mapPosition = .region(MKCoordinateRegion(
                        center: newCoord,
                        span: MKCoordinateSpan(latitudeDelta: 0.004, longitudeDelta: 0.004)
                    ))
                }
            }
        }
    }

    // MARK: - Map

    private var mapLayer: some View {
        MapReader { proxy in
            Map(position: $mapPosition) {
                UserAnnotation()

                // Manual pin — native drop pin style
                if let pin = pinnedCoordinate {
                    Marker("Search here", coordinate: pin)
                        .tint(.red)
                }

                ForEach(appState.nearbyPlaces) { place in
                    Annotation(place.name, coordinate: place.coordinate) {
                        PlaceAnnotationView(
                            place: place,
                            isSelected: selectedPlaceID == place.id
                        )
                        .onTapGesture { selectedPlaceID = place.id }
                    }
                }
            }
            .mapStyle(.standard(elevation: .realistic))
            .ignoresSafeArea()
            .simultaneousGesture(
                SpatialTapGesture()
                    .onEnded { value in
                        guard let coord = proxy.convert(value.location, from: .local) else { return }
                        UIImpactFeedbackGenerator(style: .light).impactOccurred()
                        pinnedCoordinate = coord
                        appState.searchAt(coord: coord, notificationManager: notificationManager)
                    }
            )
        }
    }

    // MARK: - Overlay

    @ViewBuilder
    private var overlayLayer: some View {
        VStack(spacing: 0) {
            if locationManager.authorizationStatus == .denied ||
               locationManager.authorizationStatus == .restricted {
                locationDeniedBanner
            }

            if appState.isSearching {
                HStack(spacing: 8) {
                    ProgressView().tint(.black).scaleEffect(0.85)
                    Text("Finding nearby places…")
                        .font(.subheadline).fontWeight(.medium)
                }
                .padding(.horizontal, 16).padding(.vertical, 10)
                .background(.ultraThinMaterial)
                .clipShape(Capsule())
                .padding(.top, 8)
                .transition(.opacity)
            }

            if let place = appState.currentPlace {
                CurrentPlaceBanner(place: place)
                    .transition(.move(edge: .bottom).combined(with: .opacity))
            }

            if !appState.recommendations.isEmpty {
                recommendationsScroll
                    .transition(.move(edge: .bottom).combined(with: .opacity))
            }
        }
        .animation(.spring(response: 0.4), value: appState.currentPlace?.id)
        .animation(.spring(response: 0.4), value: appState.recommendations.count)
        .animation(.easeInOut(duration: 0.2), value: appState.isSearching)
        .onChange(of: appState.currentPlace?.id) { _, _ in
            guard appState.currentPlace != nil else { return }
            UINotificationFeedbackGenerator().notificationOccurred(.success)
        }
    }

    private var recommendationsScroll: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 12) {
                ForEach(appState.recommendations.prefix(5)) { rec in
                    RecommendationCardView(recommendation: rec)
                        .onTapGesture {
                            UIImpactFeedbackGenerator(style: .light).impactOccurred()
                            appState.showRecommendationSheet = true
                        }
                }
            }
            .padding(.horizontal, 16)
            .padding(.vertical, 12)
        }
        .background(.ultraThinMaterial)
    }

    private var locationDeniedBanner: some View {
        HStack {
            Image(systemName: "location.slash.fill")
            Text("Location access denied. Enable it in Settings.")
                .font(.footnote)
            Spacer()
            Button("Settings") {
                if let url = URL(string: UIApplication.openSettingsURLString) {
                    UIApplication.shared.open(url)
                }
            }
            .font(.footnote).bold()
        }
        .padding()
        .background(Color.red.opacity(0.9))
        .foregroundColor(.white)
    }

    // MARK: - Toolbar

    @ToolbarContentBuilder
    private var toolbarContent: some ToolbarContent {
        ToolbarItem(placement: .navigationBarTrailing) {
            Button {
                appState.refresh(coord: locationManager.coordinate,
                                 notificationManager: notificationManager)
            } label: {
                if appState.isSearching {
                    ProgressView().tint(.indigo)
                } else {
                    Image(systemName: "arrow.clockwise")
                }
            }
        }
    }
}

// MARK: - Sub-views

struct CurrentPlaceBanner: View {
    let place: NearbyPlace

    var body: some View {
        HStack {
            Text(place.category.emoji)
                .font(.title2)
            VStack(alignment: .leading, spacing: 2) {
                Text(place.name)
                    .font(.headline)
                    .lineLimit(1)
                Text(place.category.rawValue)
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }
            Spacer()
        }
        .padding(.horizontal, 16)
        .padding(.vertical, 10)
        .background(.ultraThinMaterial)
    }
}

struct PlaceAnnotationView: View {
    let place: NearbyPlace
    let isSelected: Bool

    var body: some View {
        ZStack {
            Circle()
                .fill(isSelected ? Color.indigo : Color(.systemBackground))
                .frame(width: 36, height: 36)
                .shadow(radius: 3)
            Text(place.category.emoji)
                .font(.system(size: 18))
        }
        .scaleEffect(isSelected ? 1.3 : 1.0)
        .animation(.spring(response: 0.3), value: isSelected)
    }
}
