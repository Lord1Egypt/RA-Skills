import SwiftUI
#if canImport(FoundationModels)
import FoundationModels
#endif

struct SettingsView: View {
    @AppStorage("colorScheme") private var schemePref: String = "system"

    private var appVersion: String {
        let version = Bundle.main.infoDictionary?["CFBundleShortVersionString"] as? String ?? "—"
        let build   = Bundle.main.infoDictionary?["CFBundleVersion"] as? String ?? "—"
        return "\(version) (\(build))"
    }

    private var aiStatus: AIStatus {
        if #available(iOS 26.0, *) {
            return SystemLanguageModel.default.isAvailable ? .enabled : .disabled
        }
        return .unsupported
    }

    var body: some View {
        NavigationStack {
            Form {
                Section("Appearance") {
                    Picker("Theme", selection: $schemePref) {
                        Text("System").tag("system")
                        Text("Light").tag("light")
                        Text("Dark").tag("dark")
                    }
                    .pickerStyle(.segmented)
                }

                Section("About") {
                    LabeledContent("Version", value: appVersion)
                    LabeledContent("Location data", value: "Apple MapKit (free)")
                    LabeledContent("Cards database", value: "25 cards, 7 issuers")
                }

                SpendingProfileSection()

                TravelPreferencesSection()

                Section {
                    HStack {
                        Image(systemName: "checkmark.seal.fill").foregroundColor(.green)
                        Text("No API key required")
                    }
                    HStack {
                        Image(systemName: "dollarsign.circle.fill").foregroundColor(.green)
                        Text("Zero per-request cost")
                    }
                    HStack {
                        Image(systemName: "lock.shield.fill").foregroundColor(.blue)
                        Text("All searches stay on-device")
                    }
                } header: {
                    Text("Privacy & Cost")
                } footer: {
                    Text("Place detection uses Apple's MapKit framework — no data leaves your device to a third-party API.")
                }

                Section {
                    HStack(spacing: 12) {
                        Image(systemName: aiStatus.icon)
                            .foregroundColor(aiStatus.color)
                            .font(.title3)
                        VStack(alignment: .leading, spacing: 2) {
                            Text(aiStatus.title)
                                .font(.subheadline).fontWeight(.medium)
                            Text(aiStatus.subtitle)
                                .font(.caption).foregroundStyle(.secondary)
                        }
                    }
                    .padding(.vertical, 2)
                } header: {
                    Text("Apple Intelligence")
                } footer: {
                    Text(aiStatus.footer)
                }
            }
            .navigationTitle("Settings")
        }
    }
}

// MARK: - Spending Profile Section

struct SpendingProfileSection: View {
    @State private var profile = SpendingProfile.load()

    private let fields: [(emoji: String, label: String, keyPath: WritableKeyPath<SpendingProfile, Double>)] = [
        ("🍽️", "Dining",     \.diningMonthly),
        ("🛒", "Groceries",  \.groceriesMonthly),
        ("✈️", "Travel",     \.travelMonthly),
        ("⛽", "Gas",        \.gasMonthly),
        ("💳", "Other",      \.otherMonthly),
    ]

    var body: some View {
        Section {
            ForEach(fields, id: \.label) { field in
                SpendRow(
                    emoji: field.emoji,
                    label: field.label,
                    value: Binding(
                        get: { profile[keyPath: field.keyPath] },
                        set: { profile[keyPath: field.keyPath] = $0; profile.save() }
                    )
                )
            }

            if !profile.isEmpty {
                Button(role: .destructive) {
                    profile = SpendingProfile()
                    profile.save()
                } label: {
                    Label("Clear spending profile", systemImage: "trash")
                        .font(.subheadline)
                }
            }
        } header: {
            Text("Spending Profile")
        } footer: {
            Text(profile.isEmpty
                 ? "Tell the Ask tab your monthly spend and Fleece saves it here automatically. You can also enter values manually."
                 : "Used by the Ask tab to calculate card ROI without asking every session.")
        }
    }
}

struct SpendRow: View {
    let emoji: String
    let label: String
    @Binding var value: Double
    @State private var text: String = ""
    @FocusState private var focused: Bool

    var body: some View {
        HStack {
            Text(emoji).frame(width: 24)
            Text(label).frame(maxWidth: .infinity, alignment: .leading)
            TextField("$0", text: $text)
                .keyboardType(.decimalPad)
                .multilineTextAlignment(.trailing)
                .focused($focused)
                .foregroundColor(value > 0 ? .primary : .secondary)
                .frame(width: 80)
                .onChange(of: focused) { _, isFocused in
                    if !isFocused {
                        value = Double(text.replacingOccurrences(of: "$", with: "")) ?? 0
                        text = value > 0 ? "$\(Int(value))" : ""
                    }
                }
            Text("/mo").font(.caption).foregroundStyle(.secondary)
        }
        .onAppear {
            text = value > 0 ? "$\(Int(value))" : ""
        }
        .onChange(of: value) { _, v in
            if !focused { text = v > 0 ? "$\(Int(v))" : "" }
        }
    }
}

// MARK: - Travel Preferences Section

struct TravelPreferencesSection: View {
    @State private var profile = SpendingProfile.load()

    private static let airlinePrograms = [
        "Air Canada Aeroplan", "Alaska Mileage Plan", "American AAdvantage",
        "Air France/KLM Flying Blue", "Delta SkyMiles", "Emirates Skywards",
        "JetBlue TrueBlue", "Singapore KrisFlyer", "Southwest Rapid Rewards",
        "Turkish Miles&Smiles", "United MileagePlus", "Virgin Atlantic",
    ]

    private static let hotelPrograms = [
        "Hilton Honors", "World of Hyatt", "IHG One Rewards",
        "Marriott Bonvoy", "Wyndham Rewards",
    ]

    var body: some View {
        Section {
            Picker("Airline Program", selection: Binding(
                get: { profile.preferredAirlinePartner },
                set: { profile.preferredAirlinePartner = $0; profile.save() }
            )) {
                Text("None").tag("")
                ForEach(Self.airlinePrograms, id: \.self) { Text($0).tag($0) }
            }

            Picker("Hotel Program", selection: Binding(
                get: { profile.preferredHotelPartner },
                set: { profile.preferredHotelPartner = $0; profile.save() }
            )) {
                Text("None").tag("")
                ForEach(Self.hotelPrograms, id: \.self) { Text($0).tag($0) }
            }
        } header: {
            Text("Loyalty Programs")
        } footer: {
            Text("Tailor transfer partner and redemption recommendations to your preferred programs.")
        }
    }
}

// MARK: - AI Status

private enum AIStatus {
    case enabled, disabled, unsupported

    var icon: String {
        switch self {
        case .enabled:     return "sparkles"
        case .disabled:    return "sparkles.slash"
        case .unsupported: return "xmark.circle"
        }
    }

    var color: Color {
        switch self {
        case .enabled:     return .indigo
        case .disabled:    return .orange
        case .unsupported: return .gray
        }
    }

    var title: String {
        switch self {
        case .enabled:     return "Apple Intelligence is active"
        case .disabled:    return "Apple Intelligence is off"
        case .unsupported: return "Not available on this device"
        }
    }

    var subtitle: String {
        switch self {
        case .enabled:     return "AI card explanations enabled"
        case .disabled:    return "AI card explanations disabled"
        case .unsupported: return "Requires iOS 26 + Apple Intelligence"
        }
    }

    var footer: String {
        switch self {
        case .enabled:
            return "Fleece uses the on-device language model to generate one-sentence explanations of why a card is the best pick at each merchant. No data leaves your device."
        case .disabled:
            return "Enable Apple Intelligence in Settings → Apple Intelligence & Siri to activate AI-powered card explanations."
        case .unsupported:
            return "AI card explanations require an iPhone 15 Pro or later running iOS 26 with Apple Intelligence enabled."
        }
    }
}
