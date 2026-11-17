import Foundation

struct ChatMessage: Identifiable {
    let id = UUID()
    let role: Role
    let text: String
    let recommendedCard: String?
    let effectiveRate: Double?
    let followUp: String?

    enum Role { case user, assistant }

    // Convenience for user messages
    init(user text: String) {
        self.role = .user
        self.text = text
        self.recommendedCard = nil
        self.effectiveRate = nil
        self.followUp = nil
    }

    // Convenience for assistant messages
    init(answer: String, recommendedCard: String? = nil,
         effectiveRate: Double? = nil, followUp: String? = nil) {
        self.role = .assistant
        self.text = answer
        self.recommendedCard = recommendedCard
        self.effectiveRate = effectiveRate
        self.followUp = followUp
    }
}
