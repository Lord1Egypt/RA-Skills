// cc-sticky-notify — native macOS floating sticky note
// CLI arg: path to a content file (one line per notification line)
// Build: swiftc sticky-window.swift -o sticky-notify-app
// Usage: ./sticky-notify-app /tmp/cc-sticky-notify-myproject.txt

import Cocoa
import ApplicationServices

class StickyWindow: NSWindow {
    override var canBecomeKey: Bool { true }
    override var canBecomeMain: Bool { true }
}

// Label subclass that passes mouse events through to the parent card view.
// NSTextField normally consumes mouseDown/mouseUp, blocking the card tap.
class PassthroughLabel: NSTextField {
    override func hitTest(_ point: NSPoint) -> NSView? { nil }
}

// NSTextView subclass for meta area: supports mixed-color attributed strings,
// passes all mouse events through to the parent card view.
class PassthroughTextView: NSTextView {
    override func hitTest(_ point: NSPoint) -> NSView? { nil }
    override var acceptsFirstResponder: Bool { false }
}

// Clickable accent bar: amber = following all Spaces, slate-blue = pinned to current Space.
class AccentBarView: NSView {
    var isFollowing: Bool = false { didSet { refresh() } }
    var onToggle: ((Bool) -> Void)?
    let followColor = NSColor(calibratedRed: 0.95, green: 0.62, blue: 0.12, alpha: 1.0)
    let pinnedColor = NSColor(calibratedRed: 0.45, green: 0.55, blue: 0.70, alpha: 1.0)
    var currentColor: NSColor { isFollowing ? followColor : pinnedColor }

    override init(frame: NSRect) {
        super.init(frame: frame)
        wantsLayer = true
        refresh()
    }
    required init?(coder: NSCoder) { fatalError() }

    private func refresh() {
        layer?.backgroundColor = (isFollowing ? followColor : pinnedColor).cgColor
        toolTip = isFollowing
            ? "Following all Spaces — click to pin to current Space"
            : "Pinned to this Space — click to follow to all Spaces"
    }

    override func mouseDown(with event: NSEvent) {
        isFollowing.toggle()
        onToggle?(isFollowing)
    }
    override func acceptsFirstMouse(for event: NSEvent?) -> Bool { true }
    override func resetCursorRects() { addCursorRect(bounds, cursor: .pointingHand) }
}

// Custom card view: tracks mouseDown/mouseUp to detect a tap (not drag)
// without interfering with subview buttons or the window's move-by-background.
class StickyCardView: NSView {
    var closeBtnFrame: NSRect = .zero
    var contentFrame: NSRect = .zero   // only taps inside this area trigger focus
    var onTap: (() -> Void)?
    private var mouseDownPt: NSPoint = .zero

    override func mouseDown(with event: NSEvent) {
        mouseDownPt = convert(event.locationInWindow, from: nil)
        super.mouseDown(with: event)
    }

    override func mouseUp(with event: NSEvent) {
        let pt = convert(event.locationInWindow, from: nil)
        let dist = hypot(pt.x - mouseDownPt.x, pt.y - mouseDownPt.y)
        if dist < 5 && !closeBtnFrame.contains(pt) && contentFrame.contains(pt) {
            onTap?()
        }
        super.mouseUp(with: event)
    }

    // Accept the first mouse-down even when the window is not key,
    // so a single click triggers the tap without first activating the window.
    override func acceptsFirstMouse(for event: NSEvent?) -> Bool { true }
}

class AppDelegate: NSObject, NSApplicationDelegate {
    var window: StickyWindow!
    let contentFilePath: String
    let pidFilePath: String
    var fileWatchSource: DispatchSourceFileSystemObject?
    var headerLabel: PassthroughLabel!
    var metaLabel: PassthroughTextView!
    var focusFilePath: String
    var windowFilePath: String
    var closeBtn: NSButton!
    var collapseBtn: NSButton!
    var accentBar: AccentBarView!
    var slotFilePath: String
    var cardView: StickyCardView!
    // Overlay label shown in the center of the circle when collapsed
    var iconLabel: PassthroughLabel?
    var isCollapsed = false
    let noteW: CGFloat = 300
    let noteH: CGFloat = 102

    init(contentFilePath: String) {
        self.contentFilePath = contentFilePath
        let base = contentFilePath.hasSuffix(".txt")
            ? String(contentFilePath.dropLast(4))
            : contentFilePath
        self.pidFilePath   = base + ".pid"
        self.focusFilePath = base + ".focus"
        self.windowFilePath = base + ".window"
        self.slotFilePath  = base + ".slot"
    }

    func applicationDidFinishLaunching(_ notification: Notification) {
        // Write PID file so notify.sh can detect this running instance
        let pid = ProcessInfo.processInfo.processIdentifier
        try? String(pid).write(toFile: pidFilePath, atomically: true, encoding: .utf8)

        // NSScreen.screens[0] 始终是主屏幕（菜单栏所在屏幕），
        // 而 NSScreen.main 会随键盘焦点动态变化，不可靠
        guard let screen = NSScreen.screens.first else { NSApp.terminate(nil); return }

        let margin: CGFloat = 20
        let vis = screen.visibleFrame

        // slotStep = full window height + 8pt gap → windows never overlap
        let slotStep: CGFloat = noteH + 8
        // How many non-overlapping windows fit on this screen
        let maxNoCoverSlots = max(1, min(10, Int((vis.height - noteH - margin) / slotStep) + 1))
        let maxSlots = maxNoCoverSlots + 2  // cycling fallback pool
        var slot = 0

        var occupiedSlots = Set<Int>()
        let tmpDir = URL(fileURLWithPath: "/tmp/cc-sticky-notify")
        try? FileManager.default.createDirectory(at: tmpDir, withIntermediateDirectories: true)
        if let files = try? FileManager.default.contentsOfDirectory(at: tmpDir, includingPropertiesForKeys: nil) {
            for file in files
                where file.pathExtension == "slot" {
                let pidFile = file.deletingPathExtension().appendingPathExtension("pid")
                if let pidStr = try? String(contentsOf: pidFile, encoding: .utf8),
                   let pid = Int32(pidStr.trimmingCharacters(in: .whitespacesAndNewlines)),
                   kill(pid, 0) == 0,
                   let slotStr = try? String(contentsOf: file, encoding: .utf8),
                   let s = Int(slotStr.trimmingCharacters(in: .whitespacesAndNewlines)) {
                    occupiedSlots.insert(s)
                }
            }
        }

        if occupiedSlots.count >= maxNoCoverSlots {
            // All non-overlap slots taken — cycle via shared counter
            let cycleFile = "/tmp/cc-sticky-notify/slot"
            if let data = try? Data(contentsOf: URL(fileURLWithPath: cycleFile)),
               let str = String(data: data, encoding: .utf8),
               let n = Int(str.trimmingCharacters(in: .whitespacesAndNewlines)) {
                slot = n % maxSlots
            }
            try? String((slot + 1) % maxSlots).write(toFile: cycleFile, atomically: true, encoding: .utf8)
        } else {
            // Pick the lowest unoccupied slot in 0..<maxNoCoverSlots
            for s in 0..<maxNoCoverSlots where !occupiedSlots.contains(s) {
                slot = s
                break
            }
        }
        try? String(slot).write(toFile: slotFilePath, atomically: true, encoding: .utf8)

        let x = vis.maxX - noteW - margin
        let y = vis.maxY - noteH - margin - CGFloat(slot) * slotStep

        // 必须传入 screen 参数，否则 macOS 会忽略 contentRect 的坐标，
        // 将窗口放到鼠标当前所在屏幕
        window = StickyWindow(
            contentRect: NSRect(x: x, y: y, width: noteW, height: noteH),
            styleMask: [.borderless],
            backing: .buffered,
            defer: false,
            screen: screen
        )
        window.level = .floating
        window.isReleasedWhenClosed = false
        window.isOpaque = false
        window.backgroundColor = .clear
        window.hasShadow = true
        window.isMovableByWindowBackground = true
        window.collectionBehavior = []  // default: pinned to current Space

        // Card view: rounded corners + warm cream-yellow background
        cardView = StickyCardView(frame: NSRect(x: 0, y: 0, width: noteW, height: noteH))
        cardView.wantsLayer = true
        cardView.layer?.backgroundColor = NSColor(calibratedRed: 0.98, green: 0.96, blue: 0.72, alpha: 1.0).cgColor
        cardView.layer?.cornerRadius = 12
        cardView.layer?.masksToBounds = true
        window.contentView = cardView

        // Left accent bar: amber when following all Spaces, slate-blue when pinned
        accentBar = AccentBarView(frame: NSRect(x: 0, y: 0, width: 5, height: noteH))
        accentBar.onToggle = { [weak self] isFollowing in
            self?.window.collectionBehavior = isFollowing ? .canJoinAllSpaces : []
        }
        cardView.addSubview(accentBar)

        let rowY: CGFloat = noteH - 28

        // Header label: 13pt semibold, dark brown (same row as close/collapse buttons)
        headerLabel = PassthroughLabel(labelWithString: "")
        headerLabel.frame = NSRect(x: 16, y: rowY, width: noteW - 64, height: 20)
        headerLabel.font = NSFont.systemFont(ofSize: 13, weight: .semibold)
        headerLabel.textColor = NSColor(calibratedRed: 0.15, green: 0.10, blue: 0.0, alpha: 1.0)
        headerLabel.lineBreakMode = .byTruncatingTail
        cardView.addSubview(headerLabel)

        // Collapse button (▾, second from right in header row)
        collapseBtn = NSButton(frame: NSRect(x: noteW - 48, y: rowY + 1, width: 18, height: 18))
        collapseBtn.attributedTitle = NSAttributedString(string: "▾", attributes: [
            .foregroundColor: NSColor(calibratedRed: 0.45, green: 0.35, blue: 0.15, alpha: 0.7),
            .font: NSFont.systemFont(ofSize: 11, weight: .medium)
        ])
        collapseBtn.isBordered = false
        collapseBtn.target = self
        collapseBtn.action = #selector(collapseWindowAction)
        cardView.addSubview(collapseBtn)

        // Close button (top-right ✕, same row as header)
        closeBtn = NSButton(frame: NSRect(x: noteW - 26, y: rowY, width: 20, height: 20))
        closeBtn.attributedTitle = NSAttributedString(string: "✕", attributes: [
            .foregroundColor: NSColor(calibratedRed: 0.45, green: 0.35, blue: 0.15, alpha: 0.7),
            .font: NSFont.systemFont(ofSize: 12, weight: .medium)
        ])
        closeBtn.isBordered = false
        closeBtn.target = NSApp
        closeBtn.action = #selector(NSApplication.terminate(_:))
        cardView.addSubview(closeBtn)

        // Divider line: amber, 1pt
        let divider = NSView(frame: NSRect(x: 16, y: rowY - 4, width: noteW - 24, height: 1))
        divider.wantsLayer = true
        divider.layer?.backgroundColor = NSColor(calibratedRed: 0.85, green: 0.72, blue: 0.35, alpha: 0.7).cgColor
        cardView.addSubview(divider)

        // Meta area: NSTextView for reliable mixed-color attributed string rendering
        metaLabel = PassthroughTextView(frame: NSRect(x: 16, y: 8, width: noteW - 24, height: rowY - 16))
        metaLabel.isEditable = false
        metaLabel.isSelectable = false
        metaLabel.drawsBackground = false
        metaLabel.textContainer?.lineFragmentPadding = 0
        metaLabel.textContainerInset = .zero
        cardView.addSubview(metaLabel)

        // Load initial content from file
        let initialText = (try? String(contentsOfFile: contentFilePath, encoding: .utf8)) ?? ""
        updateLabels(from: initialText)

        // Watch content file for in-place updates when notify.sh writes new content
        let fd = open(contentFilePath, O_EVTONLY)
        if fd >= 0 {
            let source = DispatchSource.makeFileSystemObjectSource(
                fileDescriptor: fd, eventMask: .write, queue: .main)
            source.setEventHandler { [weak self] in self?.reloadContent() }
            source.setCancelHandler { close(fd) }
            source.resume()
            fileWatchSource = source
        }

        // Tap behaviour: expand when collapsed, focus terminal when expanded
        cardView.closeBtnFrame = closeBtn.frame
        cardView.contentFrame = metaLabel.frame
        cardView.onTap = { [weak self] in
            guard let self = self else { return }
            if self.isCollapsed { self.expandWindow() } else { self.focusTerminal() }
        }

        // orderFrontRegardless 不激活 App，避免系统因焦点变化重新定位窗口
        window.orderFrontRegardless()

        // Auto-close: default 1 hour; override with CC_STICKY_NOTIFY_CLOSE_TIMEOUT env var (seconds)
        let timeout: Double
        if let envVal = ProcessInfo.processInfo.environment["CC_STICKY_NOTIFY_CLOSE_TIMEOUT"],
           let seconds = Double(envVal), seconds > 0 {
            timeout = seconds
        } else {
            timeout = 3600
        }
        DispatchQueue.main.asyncAfter(deadline: .now() + timeout) {
            NSApp.terminate(nil)
        }
    }

    // Collapse: hide card content, show circle icon, shrink window.
    // Keeps cardView as contentView — avoids borderless-window contentView-swap bugs.
    @objc func collapseWindowAction() {
        guard !isCollapsed else { return }
        isCollapsed = true

        let circleSize: CGFloat = 44

        // Create a centred icon label and add it on top of cardView.
        // sizeToFit() gives the natural text size; we then place it at the circle centre.
        let icon = PassthroughLabel(labelWithString: extractIcon(from: headerLabel.stringValue))
        icon.font = NSFont.systemFont(ofSize: 22)
        icon.drawsBackground = false
        icon.isBordered = false
        icon.sizeToFit()
        let lw = max(icon.frame.width, 28), lh = max(icon.frame.height, 28)
        icon.frame = NSRect(x: (circleSize - lw) / 2, y: (circleSize - lh) / 2,
                            width: lw, height: lh)
        iconLabel = icon
        cardView.addSubview(icon)

        // Hide every other subview
        for sub in cardView.subviews where sub !== icon {
            sub.isHidden = true
        }

        // Reshape cardView layer into a circle with a coloured ring
        cardView.layer?.cornerRadius = circleSize / 2
        cardView.layer?.borderWidth = 2.5
        cardView.layer?.borderColor = accentBar.currentColor.cgColor

        // Expand tap zone to the whole circle; no close button to exclude
        cardView.closeBtnFrame = .zero
        cardView.contentFrame  = NSRect(x: 0, y: 0, width: circleSize, height: circleSize)

        // Shrink window, anchoring at the top-right corner of the original card
        let cur = window.frame
        window.setFrame(
            NSRect(x: cur.maxX - circleSize, y: cur.maxY - circleSize,
                   width: circleSize, height: circleSize),
            display: true, animate: false)
    }

    // Expand: restore card subviews and resize window back to full card.
    func expandWindow() {
        guard isCollapsed else { return }
        isCollapsed = false

        // Remove icon overlay and un-hide original subviews
        iconLabel?.removeFromSuperview()
        iconLabel = nil
        for sub in cardView.subviews {
            sub.isHidden = false
        }

        // Restore cardView layer to rounded-rect card
        cardView.layer?.cornerRadius = 12
        cardView.layer?.borderWidth = 0

        // Restore tap detection
        cardView.closeBtnFrame = closeBtn.frame
        cardView.contentFrame  = metaLabel.frame

        // Expand window, anchoring at the top-right corner of the collapsed circle
        let cur = window.frame
        window.setFrame(
            NSRect(x: cur.maxX - noteW, y: cur.maxY - noteH,
                   width: noteW, height: noteH),
            display: true, animate: false)
    }

    // Return the first grapheme cluster (emoji or character) from the header.
    func extractIcon(from text: String) -> String {
        guard let first = text.first else { return "📌" }
        return String(first)
    }

    func focusTerminal() {
        guard let raw = try? String(contentsOfFile: focusFilePath, encoding: .utf8) else { return }
        let appName = raw.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !appName.isEmpty else { return }

        guard let app = NSWorkspace.shared.runningApplications.first(where: {
            $0.executableURL?.lastPathComponent == appName || $0.localizedName == appName
        }) else { return }

        // 尝试用 Accessibility API 精准定位并激活通知触发时的那个窗口
        let windowTitle = (try? String(contentsOfFile: windowFilePath, encoding: .utf8))?
            .trimmingCharacters(in: .whitespacesAndNewlines) ?? ""

        if !windowTitle.isEmpty {
            let axApp = AXUIElementCreateApplication(app.processIdentifier)
            var windowsRef: CFTypeRef?
            if AXUIElementCopyAttributeValue(axApp, kAXWindowsAttribute as CFString, &windowsRef) == .success,
               let windows = windowsRef as? [AXUIElement] {
                for window in windows {
                    var titleRef: CFTypeRef?
                    if AXUIElementCopyAttributeValue(window, kAXTitleAttribute as CFString, &titleRef) == .success,
                       let title = titleRef as? String, title == windowTitle {
                        AXUIElementPerformAction(window, kAXRaiseAction as CFString)
                        app.activate(options: [])
                        return
                    }
                }
            }
        }

        // Fallback：无法精准匹配时直接激活 app
        app.activate(options: [])
    }

    func reloadContent() {
        guard let text = try? String(contentsOfFile: contentFilePath, encoding: .utf8) else { return }
        updateLabels(from: text)
        if isCollapsed, let icon = iconLabel {
            // Update circle icon but do NOT auto-expand
            icon.stringValue = extractIcon(from: headerLabel.stringValue)
            icon.sizeToFit()
            let cs: CGFloat = 44
            let lw = max(icon.frame.width, 28), lh = max(icon.frame.height, 28)
            icon.frame = NSRect(x: (cs - lw) / 2, y: (cs - lh) / 2, width: lw, height: lh)
        }
        animatePulse()
    }

    // Scale-bounce so the user notices the content has changed.
    func animatePulse() {
        guard let layer = window?.contentView?.layer else { return }

        if isCollapsed {
            // Shrink-first pulse so the circle stays within its 44pt bounds
            let pulse = CAKeyframeAnimation(keyPath: "transform.scale")
            pulse.values      = [1.0, 0.82, 1.0, 0.92, 1.0]
            pulse.keyTimes    = [0,   0.25, 0.5, 0.75, 1.0]
            pulse.duration    = 0.40
            pulse.repeatCount = 2
            pulse.timingFunction = CAMediaTimingFunction(name: .easeInEaseOut)
            layer.add(pulse, forKey: "updatePulse")
            return
        }

        // Expanded: scale bounce + border flash
        let pulse = CAKeyframeAnimation(keyPath: "transform.scale")
        pulse.values      = [1.0, 1.25, 0.90, 1.10, 0.96, 1.0]
        pulse.keyTimes    = [0,   0.25, 0.5,  0.7,  0.85, 1.0]
        pulse.duration    = 0.55
        pulse.repeatCount = 3
        pulse.timingFunction = CAMediaTimingFunction(name: .easeOut)
        layer.add(pulse, forKey: "updatePulse")

        let totalDuration = pulse.duration * Double(pulse.repeatCount)
        let border = CAKeyframeAnimation(keyPath: "borderWidth")
        border.values   = [0, 3.0, 3.0, 0]
        border.keyTimes = [0, 0.05, 0.9, 1.0]
        border.duration = totalDuration
        layer.borderColor = NSColor(calibratedRed: 0.95, green: 0.55, blue: 0.05, alpha: 1.0).cgColor
        layer.add(border, forKey: "updateBorder")
    }

    func updateLabels(from text: String) {
        let lines = text.components(separatedBy: "\n").filter { !$0.isEmpty }
        let headerText = lines.first ?? ""
        let metaLines = lines.dropFirst().map { line -> String in
            if let colonIdx = line.firstIndex(of: ":") {
                let key = String(line[...colonIdx])
                let value = line[line.index(after: colonIdx)...].trimmingCharacters(in: .whitespaces)
                return "\(key)\t\(value)"
            }
            return line
        }
        headerLabel.stringValue = headerText

        let metaPS = NSMutableParagraphStyle()
        metaPS.tabStops = [NSTextTab(textAlignment: .left, location: 58)]
        metaPS.lineSpacing = 3
        let normalAttrs: [NSAttributedString.Key: Any] = [
            .font: NSFont.systemFont(ofSize: 12, weight: .medium),
            .foregroundColor: NSColor(calibratedRed: 0.30, green: 0.20, blue: 0.05, alpha: 1.0),
            .paragraphStyle: metaPS
        ]
        let projectValAttrs: [NSAttributedString.Key: Any] = [
            .font: NSFont.systemFont(ofSize: 12, weight: .bold),
            .foregroundColor: NSColor(calibratedRed: 0.82, green: 0.08, blue: 0.08, alpha: 1.0),
            .paragraphStyle: metaPS
        ]
        let result = NSMutableAttributedString()
        for (i, line) in metaLines.enumerated() {
            if i > 0 { result.append(NSAttributedString(string: "\n", attributes: normalAttrs)) }
            if line.hasPrefix("Project:"), let tabIdx = line.firstIndex(of: "\t") {
                result.append(NSAttributedString(string: String(line[...tabIdx]), attributes: normalAttrs))
                result.append(NSAttributedString(string: String(line[line.index(after: tabIdx)...]), attributes: projectValAttrs))
            } else {
                result.append(NSAttributedString(string: line, attributes: normalAttrs))
            }
        }
        metaLabel.textStorage?.setAttributedString(result)
    }

    func applicationWillTerminate(_ notification: Notification) {
        fileWatchSource?.cancel()
        try? FileManager.default.removeItem(atPath: pidFilePath)
        try? FileManager.default.removeItem(atPath: focusFilePath)
        try? FileManager.default.removeItem(atPath: windowFilePath)
        try? FileManager.default.removeItem(atPath: slotFilePath)
    }

    func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool {
        return true
    }
}

let contentFilePath = CommandLine.arguments.count > 1 ? CommandLine.arguments[1] : ""
let app = NSApplication.shared
app.setActivationPolicy(.accessory)   // Hide from Dock
let delegate = AppDelegate(contentFilePath: contentFilePath)
app.delegate = delegate
app.run()
