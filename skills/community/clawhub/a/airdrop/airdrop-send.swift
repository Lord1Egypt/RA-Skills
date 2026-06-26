#!/usr/bin/env swift
import AppKit
import Foundation

enum AirDropError: Error, CustomStringConvertible {
    case noFiles
    case missingFile(String)
    case serviceUnavailable

    var description: String {
        switch self {
        case .noFiles:
            return "Provide at least one local file path."
        case .missingFile(let path):
            return "Missing file: \(path)"
        case .serviceUnavailable:
            return "AirDrop sharing service is unavailable on this Mac."
        }
    }
}

func resolveFileURLs(arguments: [String]) throws -> [URL] {
    guard !arguments.isEmpty else {
        throw AirDropError.noFiles
    }

    let manager = FileManager.default
    return try arguments.map { argument in
        let expanded = NSString(string: argument).expandingTildeInPath
        guard manager.fileExists(atPath: expanded) else {
            throw AirDropError.missingFile(expanded)
        }
        return URL(fileURLWithPath: expanded)
    }
}

do {
    let fileURLs = try resolveFileURLs(arguments: Array(CommandLine.arguments.dropFirst()))
    let app = NSApplication.shared
    app.setActivationPolicy(.accessory)
    app.activate(ignoringOtherApps: true)

    guard let service = NSSharingService(named: .sendViaAirDrop) else {
        throw AirDropError.serviceUnavailable
    }

    service.perform(withItems: fileURLs)
    print("Launched AirDrop chooser for \(fileURLs.count) item(s).")

    // Keep the process alive briefly so the sharing UI can attach cleanly.
    RunLoop.main.run(until: Date(timeIntervalSinceNow: 6))
} catch let error as AirDropError {
    fputs("AirDrop error: \(error.description)\n", stderr)
    exit(1)
} catch {
    fputs("Unexpected AirDrop error: \(error.localizedDescription)\n", stderr)
    exit(1)
}
