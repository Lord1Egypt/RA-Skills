import CoreLocation
import MapKit

enum PlacesError: LocalizedError {
    case noResults
    case searchFailed(Error)

    var errorDescription: String? {
        switch self {
        case .noResults:            return "No places found at your location."
        case .searchFailed(let e):  return e.localizedDescription
        }
    }
}

actor PlacesService {
    func nearestPlace(at coord: CLLocationCoordinate2D,
                      radius: Int = Config.detectionRadius) async throws -> NearbyPlace {
        let items = try await searchItems(at: coord, radius: radius, limit: 1)
        guard let first = items.first else { throw PlacesError.noResults }
        return first
    }

    func nearbyPlaces(at coord: CLLocationCoordinate2D,
                      radius: Int = 200,
                      limit: Int = 10) async throws -> [NearbyPlace] {
        try await searchItems(at: coord, radius: radius, limit: limit)
    }

    // MARK: - Private

    private func searchItems(at coord: CLLocationCoordinate2D,
                              radius: Int,
                              limit: Int) async throws -> [NearbyPlace] {
        let region = MKCoordinateRegion(
            center: coord,
            latitudinalMeters: Double(radius),
            longitudinalMeters: Double(radius)
        )

        // MKLocalPointsOfInterestRequest anchors strictly to the given region —
        // unlike MKLocalSearch.Request with naturalLanguageQuery which treats the
        // region as a hint and drifts toward the device's GPS location.
        let request = MKLocalPointsOfInterestRequest(coordinateRegion: region)
        request.pointOfInterestFilter = .includingAll

        do {
            let response = try await MKLocalSearch(request: request).start()
            let items = response.mapItems.prefix(limit).map { $0.toNearbyPlace() }
            guard !items.isEmpty else { throw PlacesError.noResults }
            return Array(items)
        } catch let error as PlacesError {
            throw error
        } catch {
            let mkErr = error as? MKError
            if mkErr?.code == .placemarkNotFound || mkErr?.code == .unknown {
                throw PlacesError.noResults
            }
            throw PlacesError.searchFailed(error)
        }
    }
}
