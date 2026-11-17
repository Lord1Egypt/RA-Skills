import SwiftUI

/// Horizontal scroll card shown on the home screen
struct RecommendationCardView: View {
    let recommendation: CardRecommendation

    var body: some View {
        let card = recommendation.card
        ZStack(alignment: .topLeading) {
            RoundedRectangle(cornerRadius: 16)
                .fill(card.color)
                .frame(width: 200, height: 120)
                .shadow(color: card.color.opacity(0.4), radius: 8, y: 4)

            VStack(alignment: .leading, spacing: 6) {
                HStack {
                    rankBadge
                    Spacer()
                    walletBadge
                }
                Spacer()
                Text(card.name)
                    .font(.system(size: 13, weight: .semibold))
                    .foregroundColor(card.labelColor)
                    .lineLimit(1)
                HStack(alignment: .firstTextBaseline, spacing: 2) {
                    Text(multiplierText)
                        .font(.system(size: 22, weight: .bold))
                        .foregroundColor(card.labelColor)
                    Text(recommendation.category.rawValue)
                        .font(.system(size: 11))
                        .foregroundColor(card.labelColor.opacity(0.8))
                }
                Text(rateText)
                    .font(.system(size: 11))
                    .foregroundColor(card.labelColor.opacity(0.7))
            }
            .padding(14)
            .frame(width: 200, height: 120)
        }
    }

    private var multiplierText: String {
        let m = recommendation.multiplier
        return m == m.rounded() ? "\(Int(m))x" : String(format: "%.1fx", m)
    }

    private var rateText: String {
        String(format: "≈ %.1f%% back · %@",
               recommendation.effectiveRate,
               recommendation.card.pointsProgram)
    }

    @ViewBuilder private var rankBadge: some View {
        if recommendation.rank == 1 {
            Text("BEST")
                .font(.system(size: 9, weight: .heavy))
                .padding(.horizontal, 6).padding(.vertical, 2)
                .background(Color.yellow)
                .foregroundColor(.black)
                .clipShape(Capsule())
        } else {
            Text("#\(recommendation.rank)")
                .font(.system(size: 9, weight: .semibold))
                .foregroundColor(recommendation.card.labelColor.opacity(0.7))
        }
    }

    @ViewBuilder private var walletBadge: some View {
        if recommendation.card.isInWallet {
            Image(systemName: "checkmark.circle.fill")
                .foregroundColor(.green)
                .font(.system(size: 14))
        }
    }
}

// MARK: - Full-screen recommendations sheet

struct RecommendationsSheetView: View {
    let place: NearbyPlace
    let recommendations: [CardRecommendation]
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationStack {
            List {
                Section {
                    placeHeader
                } header: {
                    Text("Location")
                }

                Section {
                    ForEach(recommendations) { rec in
                        RecommendationRowView(recommendation: rec)
                    }
                } header: {
                    Text("Best Cards · \(place.category.rawValue)")
                }
            }
            .listStyle(.insetGrouped)
            .navigationTitle("Card Recommendation")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    if let best = recommendations.first {
                        ShareLink(item: shareText(best)) {
                            Image(systemName: "square.and.arrow.up")
                        }
                    }
                }
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Done") { dismiss() }
                }
            }
        }
    }

    private func shareText(_ rec: CardRecommendation) -> String {
        let mult = rec.multiplier == rec.multiplier.rounded()
            ? "\(Int(rec.multiplier))x"
            : String(format: "%.1fx", rec.multiplier)
        let rate = String(format: "%.1f%%", rec.effectiveRate)
        return """
        \(rec.category.emoji) \(place.name)
        Use \(rec.card.name) · \(mult) \(rec.category.rawValue) = \(rate) back (\(rec.card.pointsProgram))

        via Fleece · getfleece.io/ios
        """
    }

    private var placeHeader: some View {
        HStack {
            Text(place.category.emoji)
                .font(.largeTitle)
            VStack(alignment: .leading) {
                Text(place.name).font(.headline)
                Text(place.address ?? place.category.rawValue)
                    .font(.caption).foregroundStyle(.secondary)
            }
        }
    }
}

struct RecommendationRowView: View {
    let recommendation: CardRecommendation
    @EnvironmentObject var appState: AppState
    @State private var aiExplanation: String?
    @State private var isLoadingExplanation = false

    var body: some View {
        let card = recommendation.card
        HStack(spacing: 12) {
            RoundedRectangle(cornerRadius: 8)
                .fill(card.color)
                .frame(width: 44, height: 28)
                .overlay(
                    Text(String(card.name.prefix(2)))
                        .font(.system(size: 10, weight: .bold))
                        .foregroundColor(card.labelColor)
                )

            VStack(alignment: .leading, spacing: 2) {
                HStack {
                    Text(card.name).font(.subheadline).fontWeight(.medium)
                    if recommendation.rank == 1 {
                        Text("BEST")
                            .font(.system(size: 8, weight: .heavy))
                            .padding(.horizontal, 5).padding(.vertical, 1)
                            .background(Color.yellow)
                            .foregroundColor(.black)
                            .clipShape(Capsule())
                    }
                }
                Text(card.issuer).font(.caption).foregroundStyle(.secondary)

                // Apple Intelligence explanation — only renders on iOS 18.1+
                // with Apple Intelligence enabled; invisible otherwise.
                if let explanation = aiExplanation {
                    Text(explanation)
                        .font(.caption)
                        .foregroundStyle(.indigo.opacity(0.8))
                        .fixedSize(horizontal: false, vertical: true)
                        .transition(.opacity)
                } else if isLoadingExplanation {
                    HStack(spacing: 4) {
                        ProgressView().scaleEffect(0.6)
                        Text("Analyzing…")
                            .font(.caption2)
                            .foregroundStyle(.tertiary)
                    }
                }
            }

            Spacer()

            VStack(alignment: .trailing, spacing: 2) {
                Text(multiplierText)
                    .font(.system(size: 17, weight: .bold))
                    .foregroundColor(.indigo)
                Text(String(format: "%.1f%%", recommendation.effectiveRate))
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }

            Image(systemName: card.isInWallet ? "checkmark.circle.fill" : "circle")
                .foregroundColor(card.isInWallet ? .green : .gray)
                .onTapGesture { appState.toggleWallet(card: card) }
        }
        .padding(.vertical, 4)
        .task(id: recommendation.card.id) {
            await loadExplanation()
        }
        .animation(.easeIn(duration: 0.2), value: aiExplanation)
    }

    private func loadExplanation() async {
        guard #available(iOS 26.0, *) else { return }
        isLoadingExplanation = true
        aiExplanation = await CardExplanationService.shared.explanation(for: recommendation)
        isLoadingExplanation = false
    }

    private var multiplierText: String {
        let m = recommendation.multiplier
        return m == m.rounded() ? "\(Int(m))x" : String(format: "%.1fx", m)
    }
}
