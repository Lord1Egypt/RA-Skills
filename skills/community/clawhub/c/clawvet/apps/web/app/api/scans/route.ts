import { NextRequest, NextResponse } from "next/server";

const API_URL = process.env.API_URL || "http://localhost:3001";

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const limit = searchParams.get("limit") || "20";
    const offset = searchParams.get("offset") || "0";

    const res = await fetch(
      `${API_URL}/api/v1/scans?limit=${limit}&offset=${offset}`,
      { cache: "no-store" }
    );

    if (!res.ok) {
      return NextResponse.json(
        { scans: [], error: "API unavailable" },
        { status: 200 }
      );
    }

    const data = await res.json();
    return NextResponse.json(data);
  } catch {
    return NextResponse.json({ scans: [] }, { status: 200 });
  }
}
