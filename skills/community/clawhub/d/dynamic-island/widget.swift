import Cocoa
import WebKit

// MARK: - Hover tracking view

class HoverView: NSView {
    var onEnter: (() -> Void)?
    var onExit: (() -> Void)?
    var onMove: ((NSPoint) -> Void)?

    override func updateTrackingAreas() {
        super.updateTrackingAreas()
        trackingAreas.forEach { removeTrackingArea($0) }
        let area = NSTrackingArea(
            rect: bounds,
            options: [.mouseEnteredAndExited, .mouseMoved, .activeAlways, .inVisibleRect],
            owner: self,
            userInfo: nil
        )
        addTrackingArea(area)
    }

    override func mouseEntered(with event: NSEvent) { onEnter?() }
    override func mouseExited(with event: NSEvent) { onExit?() }
    override func mouseMoved(with event: NSEvent) {
        let loc = convert(event.locationInWindow, from: nil)
        onMove?(loc)
    }
    override func hitTest(_ point: NSPoint) -> NSView? { return nil }
    override var acceptsFirstResponder: Bool { return false }
}

// MARK: - App Delegate

class AppDelegate: NSObject, NSApplicationDelegate, WKScriptMessageHandler {
    var window: NSPanel!
    var webView: WKWebView!
    var visualEffect: NSVisualEffectView!
    var hoverView: HoverView!

    func applicationDidFinishLaunching(_ notification: Notification) {
        NSApp.activate(ignoringOtherApps: true)

        let w: CGFloat = 180
        let h: CGFloat = 38

        let visible = NSScreen.main!.visibleFrame
        let origin = NSPoint(
            x: visible.midX - w / 2,
            y: visible.maxY - h - 2
        )

        window = NSPanel(
            contentRect: NSRect(origin: origin, size: NSSize(width: w, height: h)),
            styleMask: [.borderless, .nonactivatingPanel, .utilityWindow],
            backing: .buffered,
            defer: false
        )

        window.level = NSWindow.Level(Int(CGShieldingWindowLevel()))
        window.isOpaque = false
        window.backgroundColor = .clear
        window.hasShadow = true
        window.isMovableByWindowBackground = false
        window.collectionBehavior = [.canJoinAllSpaces, .stationary, .fullScreenAuxiliary]
        window.hidesOnDeactivate = false

        window.contentView?.wantsLayer = true
        window.contentView?.layer?.cornerRadius = h / 2
        window.contentView?.layer?.masksToBounds = true

        visualEffect = NSVisualEffectView(frame: NSRect(origin: .zero, size: NSSize(width: w, height: h)))
        visualEffect.material = .toolTip
        visualEffect.appearance = NSAppearance(named: .darkAqua)
        visualEffect.blendingMode = .behindWindow
        visualEffect.state = .active
        visualEffect.autoresizingMask = [.width, .height]

        let config = WKWebViewConfiguration()
        config.userContentController.add(self, name: "shake")
        config.userContentController.add(self, name: "resize")
        config.userContentController.add(self, name: "openURL")
        config.mediaTypesRequiringUserActionForPlayback = []

        webView = WKWebView(
            frame: NSRect(origin: .zero, size: NSSize(width: w, height: h)),
            configuration: config
        )
        webView.setValue(false, forKey: "drawsBackground")
        webView.autoresizingMask = [.width, .height]

        let port = ProcessInfo.processInfo.environment["OPENCLAW_HTTP_PORT"] ?? "7788"
        let url = URL(string: "http://localhost:\(port)/?widget")!
        webView.load(URLRequest(url: url))

        visualEffect.addSubview(webView)
        window.contentView?.addSubview(visualEffect)

        // HoverView — tracks mouse, passes clicks through
        hoverView = HoverView(frame: NSRect(origin: .zero, size: NSSize(width: w, height: h)))
        hoverView.autoresizingMask = [.width, .height]
        hoverView.onEnter = { [weak self] in
            self?.webView.evaluateJavaScript("handleHoverEnter()")
        }
        hoverView.onExit = { [weak self] in
            self?.webView.evaluateJavaScript("handleHoverLeave()")
        }
        hoverView.onMove = { [weak self] loc in
            // Convert AppKit coords (origin bottom-left) to webview coords (origin top-left)
            guard let self = self else { return }
            let frameHeight = self.hoverView.bounds.height
            let webY = frameHeight - loc.y
            self.webView.evaluateJavaScript("handleHoverMove(\(loc.x), \(webY))")
        }
        window.contentView?.addSubview(hoverView)

        window.orderFrontRegardless()
    }

    // MARK: - WKScriptMessageHandler

    func userContentController(_ userContentController: WKUserContentController, didReceive message: WKScriptMessage) {
        if message.name == "shake" {
            let type = message.body as? String ?? "done"
            webView.evaluateJavaScript("document.body.style.animation='none';void document.body.offsetHeight;document.body.style.animation='css-shake 0.4s ease'", completionHandler: nil)
            if type == "error" {
                playSound("/System/Library/Sounds/Basso.aiff")
            } else {
                playSound("/System/Library/Sounds/Glass.aiff")
            }
        } else if message.name == "openURL", let urlStr = message.body as? String,
                  let url = URL(string: urlStr) {
            NSWorkspace.shared.open(url)
        } else if message.name == "resize", let body = message.body as? [String: Any] {
            let w = body["w"] as? CGFloat ?? 180
            let h = body["h"] as? CGFloat ?? 38
            let r = body["radius"] as? CGFloat ?? 19
            resizeWindow(to: w, height: h, radius: r)
        }
    }

    func resizeWindow(to width: CGFloat, height: CGFloat, radius: CGFloat) {
        let visible = NSScreen.main!.visibleFrame
        let newFrame = NSRect(
            x: visible.midX - width / 2,
            y: visible.maxY - height - 2,
            width: width,
            height: height
        )
        NSAnimationContext.runAnimationGroup { ctx in
            ctx.duration = 0.3
            ctx.timingFunction = CAMediaTimingFunction(name: .easeInEaseOut)
            self.window.animator().setFrame(newFrame, display: true)
        }
        window.contentView?.layer?.cornerRadius = radius
    }

    func playSound(_ path: String) {
        if let sound = NSSound(contentsOfFile: path, byReference: true) {
            sound.play()
        }
    }

}

let app = NSApplication.shared
app.setActivationPolicy(.accessory)
let delegate = AppDelegate()
app.delegate = delegate
app.run()
