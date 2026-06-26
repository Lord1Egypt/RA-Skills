import { NextRequest, NextResponse } from "next/server";

const API_URL = process.env.API_URL || "http://localhost:3001";

export async function GET(request: NextRequest) {
  try {
    const cookie = request.cookies.get("cg_session")?.value;
    if (!cookie) {
      return NextResponse.json({ user: null }, { status: 200 });
    }

    const res = await fetch(`${API_URL}/api/v1/auth/me`, {
      headers: { Cookie: `cg_session=${cookie}` },
      cache: "no-store",
    });

    if (!res.ok) {
      return NextResponse.json({ user: null }, { status: 200 });
    }

    const user = await res.json();
    return NextResponse.json({ user });
  } catch {
    return NextResponse.json({ user: null }, { status: 200 });
  }
}
