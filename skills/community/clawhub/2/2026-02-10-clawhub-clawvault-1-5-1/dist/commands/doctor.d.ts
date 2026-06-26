type DoctorStatus = 'ok' | 'warn' | 'error';
interface DoctorCheck {
    label: string;
    status: DoctorStatus;
    detail?: string;
    hint?: string;
}
interface DoctorReport {
    vaultPath?: string;
    checks: DoctorCheck[];
    warnings: number;
    errors: number;
}
declare function doctor(vaultPath?: string): Promise<DoctorReport>;

export { type DoctorCheck, type DoctorReport, type DoctorStatus, doctor };
