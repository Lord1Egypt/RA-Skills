import CoreLocation
import MapKit

struct NearbyPlace: Identifiable, Equatable {
    let id: String              // "\(lat),\(lng)" — stable enough for dedup
    let name: String
    let placeTypes: [String]    // unused with MapKit; kept for future extensibility
    let coordinate: CLLocationCoordinate2D
    let rating: Double?
    let address: String?
    let category: MCCCategory

    static func == (lhs: NearbyPlace, rhs: NearbyPlace) -> Bool {
        lhs.id == rhs.id
    }
}

// MARK: - MKMapItem → NearbyPlace

extension MKMapItem {
    func toNearbyPlace() -> NearbyPlace {
        let coord = placemark.coordinate
        return NearbyPlace(
            id: String(format: "%.5f,%.5f", coord.latitude, coord.longitude),
            name: name ?? placemark.name ?? "Unknown",
            placeTypes: [],
            coordinate: coord,
            rating: nil,
            address: placemark.formattedAddress,
            category: MCCCategory.from(poiCategory: pointOfInterestCategory)
        )
    }
}

extension MKPlacemark {
    var formattedAddress: String? {
        [subThoroughfare, thoroughfare, locality]
            .compactMap { $0 }
            .filter { !$0.isEmpty }
            .joined(separator: " ")
            .nilIfEmpty
    }
}

private extension String {
    var nilIfEmpty: String? { isEmpty ? nil : self }
}
