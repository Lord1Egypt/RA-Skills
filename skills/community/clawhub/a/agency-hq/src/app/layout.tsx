import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Agency HQ — AI Agent Office",
  description: "A pixel art office where your AI agents work, chat, and ship — live. Built for OpenClaw.",
  openGraph: {
    title: "Agency HQ — AI Agent Office",
    description: "Watch your AI agents work in a pixel art office. Real-time status, activity feed, and agent banter.",
    images: ["/og-image.png"],
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "Agency HQ — AI Agent Office",
    description: "Watch your AI agents work in a pixel art office. Real-time status, activity feed, and agent banter.",
    images: ["/og-image.png"],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="bg-[#0a0a0f] text-[#e0e0e0] antialiased">
        {children}
      </body>
    </html>
  );
}
