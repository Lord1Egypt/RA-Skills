import SwiftUI
import CoreLocation
import Combine
import PassKit
import WidgetKit

@MainActor
final class AppState: ObservableObject {
    // Current nearest place & its recommendations
    @Published var currentPlace: NearbyPlace?
    @Published var recommendations: [CardRecommendation] = []
    @Published var isSearching = false
    @Published var searchError: String?

    // Nearby pins for the map
    @Published var nearbyPlaces: [NearbyPlace] = []

    // All cards (wallet state persisted in UserDefaults)
    @Published var cards: [CreditCard] = [] {
        didSet { persistWallet() }
    }

    // Tab selection — tapping a notification deep-links to .recommendations
    @Published var selectedTab: Tab = .home
    @Published var showRecommendationSheet = false

    // Network detection
    @Published var detectedNetworks: Set<PKPaymentNetwork> = []
    @Published var suggestedCards: [CreditCard] = []

    // Annual fee renewal dates — keyed by card UUID string
    @Published var renewalDates: [String: Date] = [:]

    enum Tab: Hashable { case home, wallet, ask, settings }

    private let placesService = PlacesService()
    private var searchTask: Task<Void, Never>?
    private var lastSearchedCoord: CLLocationCoordinate2D?

    init() {
        cards = loadWallet()
        renewalDates = loadRenewalDates()
        runWalletDetection()
    }

    func runWalletDetection() {
        let result = WalletDetectionService.detect(cards: cards)
        detectedNetworks = result.detectedNetworks
        suggestedCards = result.suggestedCards
    }

    // MARK: - Location-triggered search

    func onLocationUpdate(_ coord: CLLocationCoordinate2D,
                          notificationManager: NotificationManager) {
        // Debounce: only re-search if we've moved > 30 m
        if let last = lastSearchedCoord,
           distanceMeters(last, coord) < 30 { return }
        lastSearchedCoord = coord

        searchTask?.cancel()
        searchTask = Task {
            await searchPlaces(at: coord,
                               notificationManager: notificationManager)
        }
    }

    private func searchPlaces(at coord: CLLocationCoordinate2D,
                               notificationManager: NotificationManager,
                               radius: Int = Config.detectionRadius,
                               notify: Bool = true) async {
        isSearching = true
        searchError = nil
        do {
            async let nearest = placesService.nearestPlace(at: coord, radius: radius)
            async let nearby  = placesService.nearbyPlaces(at: coord, radius: max(radius, 200))

            let (place, pins) = try await (nearest, nearby)

            let recs = CardRecommender.recommend(for: place, cards: cards)
            currentPlace    = place
            recommendations = recs
            nearbyPlaces    = pins

            let bestCard = recs.first(where: { $0.card.isInWallet }) ?? recs.first

            if notify, let best = bestCard {
                notificationManager.notify(recommendation: best)
            }

            if let best = bestCard {
                saveWidgetData(recommendation: best)
            }
        } catch PlacesError.noResults {
            searchError = nil   // silently ignore; user might be outdoors
        } catch {
            searchError = error.localizedDescription
        }
        isSearching = false
    }

    // MARK: - Manual refresh

    func refresh(coord: CLLocationCoordinate2D?,
                 notificationManager: NotificationManager) {
        guard let coord else { return }
        lastSearchedCoord = nil
        onLocationUpdate(coord, notificationManager: notificationManager)
    }

    // Search at an arbitrary tapped coordinate (bypasses debounce, larger radius, no notification)
    func searchAt(coord: CLLocationCoordinate2D,
                  notificationManager: NotificationManager) {
        searchTask?.cancel()
        searchTask = Task {
            await searchPlaces(at: coord,
                               notificationManager: notificationManager,
                               radius: 300,
                               notify: false)
        }
    }

    // MARK: - Wallet persistence

    func toggleWallet(card: CreditCard) {
        guard let idx = cards.firstIndex(where: { $0.id == card.id }) else { return }
        cards[idx].isInWallet.toggle()
        if let place = currentPlace {
            recommendations = CardRecommender.recommend(for: place, cards: cards)
            if let best = recommendations.first(where: { $0.card.isInWallet }) ?? recommendations.first {
                saveWidgetData(recommendation: best)
            }
        }
        runWalletDetection()
        saveFeeCalendarWidgetData()
    }

    private func saveWidgetData(recommendation: CardRecommendation) {
        FleeceWidgetData(
            cardName: recommendation.card.name,
            cardColor: recommendation.card.cardColor,
            textColor: recommendation.card.textColor,
            multiplier: recommendation.multiplier,
            categoryEmoji: recommendation.category.emoji,
            categoryName: recommendation.category.rawValue,
            placeName: recommendation.place.name,
            rewardRate: recommendation.effectiveRate,
            updatedAt: .now
        ).save()
        WidgetCenter.shared.reloadAllTimelines()
    }

    private func persistWallet() {
        let walletIDs = cards.filter(\.isInWallet).map(\.id.uuidString)
        UserDefaults.standard.set(walletIDs, forKey: "fleeceWallet")
    }

    private func loadWallet() -> [CreditCard] {
        let walletIDs = Set(
            UserDefaults.standard.stringArray(forKey: "fleeceWallet") ?? []
        )
        return CardDatabase.all.map { card in
            var c = card
            c.isInWallet = walletIDs.contains(card.id.uuidString)
            return c
        }
    }

    // MARK: - Renewal dates

    func renewalDate(for card: CreditCard) -> Date? {
        renewalDates[card.id.uuidString]
    }

    func setRenewalDate(_ date: Date?, for card: CreditCard) {
        if let date {
            renewalDates[card.id.uuidString] = date
        } else {
            renewalDates.removeValue(forKey: card.id.uuidString)
        }
        persistRenewalDates()
        saveFeeCalendarWidgetData()
    }

    private func persistRenewalDates() {
        let raw = renewalDates.mapValues { $0.timeIntervalSince1970 }
        UserDefaults.standard.set(raw, forKey: "fleeceRenewalDates")
    }

    func saveFeeCalendarWidgetData() {
        let cal   = Calendar.current
        let today = cal.startOfDay(for: .now)
        let items: [FeeCalendarWidgetData.RenewalItem] = cards
            .filter { $0.isInWallet && $0.annualFee > 0 }
            .compactMap { card in
                guard let date = renewalDates[card.id.uuidString] else { return nil }
                var next = cal.startOfDay(for: date)
                while next < today {
                    next = cal.date(byAdding: .year, value: 1, to: next)!
                }
                let days = cal.dateComponents([.day], from: today, to: next).day ?? 0
                return FeeCalendarWidgetData.RenewalItem(
                    cardName:        card.name,
                    cardColor:       card.cardColor,
                    textColor:       card.textColor,
                    annualFee:       card.annualFee,
                    nextRenewalDate: next,
                    daysUntil:       days
                )
            }
            .sorted { $0.daysUntil < $1.daysUntil }

        FeeCalendarWidgetData(renewals: items, updatedAt: .now).save()
        WidgetCenter.shared.reloadTimelines(ofKind: "FeeCalendarWidget")
    }

    private func loadRenewalDates() -> [String: Date] {
        let raw = UserDefaults.standard.dictionary(forKey: "fleeceRenewalDates") as? [String: Double] ?? [:]
        return raw.mapValues { Date(timeIntervalSince1970: $0) }
    }

    // MARK: - Util

    private func distanceMeters(_ a: CLLocationCoordinate2D,
                                 _ b: CLLocationCoordinate2D) -> Double {
        let loc1 = CLLocation(latitude: a.latitude, longitude: a.longitude)
        let loc2 = CLLocation(latitude: b.latitude, longitude: b.longitude)
        return loc1.distance(from: loc2)
    }
}

