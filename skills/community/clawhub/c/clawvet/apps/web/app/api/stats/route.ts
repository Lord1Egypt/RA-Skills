import { NextResponse } from "next/server";

const API_URL = process.env.API_URL || "http://localhost:3001";

export async function GET() {
  try {
    const res = await fetch(`${API_URL}/api/v1/stats`, {
      cache: "no-store",
    });

    if (!res.ok) {
      return NextResponse.json({
        skillsScanned: 0,
        threatsFound: 0,
        avgRiskScore: 0,
      });
    }

    const data = await res.json();
    return NextResponse.json(data);
  } catch {
    return NextResponse.json({
      skillsScanned: 0,
      threatsFound: 0,
      avgRiskScore: 0,
    });
  }
}
