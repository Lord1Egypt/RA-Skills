import SwiftUI

struct AskView: View {
    @EnvironmentObject var appState: AppState
    @StateObject private var chat = ChatService()
    @State private var input = ""
    @State private var scrollID: UUID?
    @FocusState private var inputFocused: Bool

    private let suggestions = [
        "Which card is best for dining?",
        "Where can I transfer my Chase points?",
        "Does Sapphire Reserve cover rental cars?",
        "How much are my Hyatt points worth?",
        "Which cards get me into airport lounges?",
    ]

    var body: some View {
        NavigationStack {
            VStack(spacing: 0) {
                messageList
                inputBar
            }
            .navigationTitle("Ask Fleece")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    if !chat.messages.isEmpty {
                        Button("Clear") { chat.clear() }
                            .font(.subheadline)
                    }
                }
            }
        }
        .onAppear { chat.setCards(appState.cards) }  // initial load only
        .onChange(of: appState.cards.filter(\.isInWallet).map(\.id)) { _, _ in
            chat.setCards(appState.cards)              // only when wallet membership changes
        }
    }

    // MARK: - Message list

    private var messageList: some View {
        ScrollViewReader { proxy in
            ScrollView {
                LazyVStack(spacing: 12) {
                    if chat.messages.isEmpty {
                        emptyState
                    } else {
                        ForEach(chat.messages) { msg in
                            MessageBubble(message: msg) { suggestion in
                                sendMessage(suggestion)
                            }
                            .id(msg.id)
                        }
                        if chat.isThinking {
                            ThinkingBubble()
                                .id("thinking")
                        }
                    }
                }
                .padding(.horizontal, 16)
                .padding(.vertical, 12)
            }
            .onChange(of: chat.messages.count) { _, _ in
                withAnimation {
                    if let lastID = chat.messages.last?.id {
                        proxy.scrollTo(lastID, anchor: .bottom)
                    }
                }
            }
            .onChange(of: chat.isThinking) { _, _ in
                withAnimation { proxy.scrollTo("thinking", anchor: .bottom) }
            }
        }
    }

    // MARK: - Empty state with suggestions

    private var emptyState: some View {
        VStack(spacing: 20) {
            Spacer().frame(height: 40)
            Image(systemName: "bubble.left.and.bubble.right")
                .font(.system(size: 48))
                .foregroundStyle(.secondary)

            VStack(spacing: 6) {
                Text("Ask Fleece")
                    .font(.title3).fontWeight(.semibold)
                Text("Your private, on-device card advisor.")
                    .font(.subheadline).foregroundStyle(.secondary)
            }

            VStack(spacing: 10) {
                ForEach(suggestions, id: \.self) { suggestion in
                    Button {
                        sendMessage(suggestion)
                    } label: {
                        Text(suggestion)
                            .font(.subheadline)
                            .foregroundColor(.indigo)
                            .padding(.horizontal, 16).padding(.vertical, 10)
                            .frame(maxWidth: .infinity, alignment: .leading)
                            .background(Color.indigo.opacity(0.08))
                            .clipShape(RoundedRectangle(cornerRadius: 12))
                    }
                }
            }
            .padding(.top, 8)
        }
        .padding(.horizontal, 4)
    }

    // MARK: - Input bar

    private var inputBar: some View {
        VStack(spacing: 0) {
            Divider()
            HStack(spacing: 10) {
                TextField("Ask about your cards…", text: $input, axis: .vertical)
                    .lineLimit(1...4)
                    .focused($inputFocused)
                    .submitLabel(.send)
                    .onSubmit { sendMessage(input) }
                    .padding(.horizontal, 14)
                    .padding(.vertical, 10)
                    .background(Color(.systemGray6))
                    .clipShape(RoundedRectangle(cornerRadius: 20))

                Button {
                    sendMessage(input)
                } label: {
                    Image(systemName: "arrow.up.circle.fill")
                        .font(.system(size: 32))
                        .foregroundColor(input.trimmingCharacters(in: .whitespaces).isEmpty || chat.isThinking
                                         ? .gray.opacity(0.4) : .indigo)
                }
                .disabled(input.trimmingCharacters(in: .whitespaces).isEmpty || chat.isThinking)
            }
            .padding(.horizontal, 16)
            .padding(.vertical, 10)
            .background(.ultraThinMaterial)
        }
    }

    private func sendMessage(_ text: String) {
        let trimmed = text.trimmingCharacters(in: .whitespaces)
        guard !trimmed.isEmpty else { return }
        input = ""
        inputFocused = false
        Task { await chat.send(trimmed) }
    }
}

// MARK: - Message bubble

struct MessageBubble: View {
    let message: ChatMessage
    let onFollowUpTap: (String) -> Void

    var body: some View {
        VStack(alignment: message.role == .user ? .trailing : .leading, spacing: 6) {
            HStack {
                if message.role == .user { Spacer(minLength: 60) }

                Text(message.text)
                    .font(.subheadline)
                    .foregroundColor(message.role == .user ? .white : .primary)
                    .padding(.horizontal, 14)
                    .padding(.vertical, 10)
                    .background(message.role == .user ? Color.indigo : Color(.systemGray6))
                    .clipShape(RoundedRectangle(cornerRadius: 18))

                if message.role == .assistant { Spacer(minLength: 60) }
            }

            // Card chip — shown when model recommended a specific card
            if let card = message.recommendedCard,
               let rate = message.effectiveRate,
               message.role == .assistant {
                HStack(spacing: 6) {
                    Image(systemName: "creditcard.fill")
                        .font(.caption)
                        .foregroundColor(.indigo)
                    Text(card)
                        .font(.caption).fontWeight(.semibold)
                    Text("·")
                        .foregroundStyle(.secondary)
                    Text(String(format: "%.1f%% back", rate))
                        .font(.caption)
                        .foregroundColor(.indigo)
                }
                .padding(.horizontal, 12).padding(.vertical, 6)
                .background(Color.indigo.opacity(0.08))
                .clipShape(Capsule())
            }

            // Follow-up suggestion pill
            if let followUp = message.followUp, message.role == .assistant {
                Button {
                    onFollowUpTap(followUp)
                } label: {
                    HStack(spacing: 4) {
                        Image(systemName: "arrow.turn.down.right")
                            .font(.caption2)
                        Text(followUp)
                            .font(.caption)
                    }
                    .foregroundColor(.indigo)
                    .padding(.horizontal, 12).padding(.vertical, 6)
                    .background(Color.indigo.opacity(0.08))
                    .clipShape(Capsule())
                }
            }
        }
        .frame(maxWidth: .infinity, alignment: message.role == .user ? .trailing : .leading)
    }
}

// MARK: - Thinking indicator

struct ThinkingBubble: View {
    @State private var phase = 0

    var body: some View {
        HStack(spacing: 4) {
            ForEach(0..<3, id: \.self) { i in
                Circle()
                    .fill(Color.secondary.opacity(0.5))
                    .frame(width: 7, height: 7)
                    .scaleEffect(phase == i ? 1.3 : 1.0)
                    .animation(.easeInOut(duration: 0.4).repeatForever().delay(Double(i) * 0.15),
                               value: phase)
            }
        }
        .padding(.horizontal, 16).padding(.vertical, 12)
        .background(Color(.systemGray6))
        .clipShape(RoundedRectangle(cornerRadius: 18))
        .frame(maxWidth: .infinity, alignment: .leading)
        .onAppear { phase = 2 }
    }
}
