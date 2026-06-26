export type BaziGender = "male" | "female";
export type CalendarType = "solar" | "lunar";
export type AccuracyMode = "full_chart" | "missing_time_six_pillars";
export interface BaziCalcInput {
    name: string;
    date: string;
    time?: string;
    location: string;
    gender: BaziGender;
    calendarType: CalendarType;
    sect: 1 | 2;
    sourceCommand: "/bazi-persona create" | "/bazi-persona update";
    trueSolarMode?: "auto" | "on" | "off";
    longitude?: number;
    dayRolloverHour?: number;
}
interface Pillars {
    year?: string;
    month?: string;
    day?: string;
    hour?: string;
}
export interface BaziChart {
    schema_version: string;
    generated_at: string;
    source_command: string;
    accuracy_mode: AccuracyMode;
    requires_birth_time_for_full_accuracy: boolean;
    notes: string[];
    birth_input: {
        name: string;
        date: string;
        provided_time?: string;
        clock_time: string;
        true_solar_time?: string;
        time_correction_minutes?: number;
        effective_time: string;
        location: string;
        longitude?: number;
        true_solar_mode?: "auto" | "on" | "off";
        day_rollover_hour?: number;
        gender: BaziGender;
        calendar_type: CalendarType;
        sect: 1 | 2;
    };
    pillars: Pillars;
    day_master?: string;
    five_elements: unknown;
    ten_gods: unknown;
    luck_cycles: unknown;
    current_year: number;
    yearly_fortune: unknown;
    removed_due_to_missing_time: string[];
    raw_markdown: string;
    raw_bazi: unknown;
}
export declare function normalizeDateInput(rawDate: string): string;
export declare function validateDate(date: string): void;
export declare function validateTime(time: string): void;
export declare function normalizeTimeInput(rawTime: string): string;
export declare function buildChart(input: BaziCalcInput): Promise<BaziChart>;
export {};
