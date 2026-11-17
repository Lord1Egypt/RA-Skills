import Foundation

enum Config {
    // How close (meters) to a place to trigger detection
    static let detectionRadius: Int = 60

    // Don't re-fire a notification for the same place within this window (seconds)
    static let notificationCooldown: TimeInterval = 300
}
